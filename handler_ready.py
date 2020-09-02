import pymongo
from pymongo import MongoClient
import requests
import json
import time
import math
from datetime import datetime
from const import *

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_stats = mongo_db.users_stats

def handler_ready(bot,message,my_logger):

	try:

		if message.text == '!готовность':

			bot.reply_to(message, msg_ready_help, parse_mode='Markdown')
			my_logger.info("Info about readiness command sent")

		else:

			s = message.text.split()
			pers = s[1].lower()

			if pers in REQS_ALIASES:

				pers_id = REQS_ALIASES[pers]

				row = collection_stats.find() # соберем всю стату которая есть
				count_row = collection_stats.count_documents({}) # сколько всего игроков в базе в данный момент
				already_have7 = []
				already_have6 = []
				already_have5 = []
				not_have7 = []
				not_have_at_all = []
				current_time = math.floor(time.time())

				# возьмем last_update у первого игрока в списке (предполагаем что у всех должно быть одинаково)
				# last_update = datetime.fromtimestamp(row[0]['last_update']).strftime('%d-%m-%Y %H:%M:%S')
				last_update = row[0]['last_update']
				passed_time = current_time-last_update

				if passed_time<60:
					passed_time_text = f"{passed_time} сек"
				elif passed_time<3600:
					passed_time_text = f"{passed_time//60} мин"
				elif passed_time<86400:
					passed_time_text = f"{passed_time//3600} ч"
				else:
					passed_time_text = "более 1 дня"

				msg = f'(обновлено с сайта swgoh.gg *{passed_time_text} назад*)\n\n'
				msg += f'У меня есть информация о `{count_row}` игроках гильдии\n\n'

				# для начала пройдемся по всем игрокам и соберем инфу у кого уже есть и на сколько звезд
				for r in row: # каждая отдельная имеющаяся стата
					if pers_id in r: # искомый легендарный персонаж имеется в стате игрока
						if r[pers_id] == 7: # и у него 7 звезд
							already_have7.append(r['player_name'])
						elif r[pers_id] == 6:
							already_have6.append(r['player_name'])
							not_have7.append(r['player_name'])
						elif r[pers_id] == 5:
							already_have5.append(r['player_name'])
							not_have7.append(r['player_name'])
						else:
							not_have7.append(r['player_name'])
					else:
						not_have7.append(r['player_name'])
						not_have_at_all.append(r['player_name'])

				# в итоге в not_have7 будут все, у кого не на 7 звезд

				if len(already_have7) > 0 or len(already_have6) > 0 or len(already_have5) > 0:
					msg += f'Из них *{len(already_have7)}* уже имеют данного персонажа на `7` звезд:\n_{", ".join(already_have7)}_\n\n'
					if len(already_have6) > 0:
						msg += f'Еще *{len(already_have6)}* — на `6` звезд:\n_{", ".join(already_have6)}_\n\n'
					if len(already_have5) > 0:
						msg += f'И еще *{len(already_have5)}* — на `5` звезд:\n_{", ".join(already_have5)}_\n\n'
				else:
					msg += f'*Ни у кого из гильдии нет этого персонажа!*\n\n'


				if not pers_id in REQS: # если не нужно проверять готовность к ивенту (вампа, хода, трея), то сразу напишем у кого нет вообще
					msg += f'Список тех, у кого нет вообще:\n_{", ".join(not_have_at_all)}_'


				if pers_id == "JEDIKNIGHTLUKE":

					msg_improve = ""

					if len(not_have7) > 0:

						not_have7_copy = not_have7[:]  # в not_have7_copy список игроков, которые еще не получили персонажа
						msg += f'Кто во время следующего события сможет взять этого персонажа или улучшить по звездам'
						msg += ':\n\n'

						for nh in not_have7:

							found_user_stat = collection_stats.find_one({"player_name": nh})
							stars = {}
							relic = {}

							for req in REQS[pers_id]:
								if req in found_user_stat:
									if found_user_stat[req+"_relic"]:
										relic[req] = int(found_user_stat[req+"_relic"])-1
									else:
										relic[req] = 0
								else:
									relic[req] = 0

							readiness_percent = 0

							for req in REQS[pers_id]: # идем по полному списку требований на люка
								if req in relic:
									if relic[req] >= 3:
										readiness_percent += 11
									else:
										pass

							if readiness_percent == 99:
								msg_improve += f"`{nh}`: \u2605 \u2605 \u2605 \u2605 \u2605 \u2605 \u2605 \n" # записываем, что этот игрок получит на 7 звезд
								not_have7_copy.remove(nh) # убираем его из списка тех, кто не получит

					if msg_improve == "":
						if count_row == len(already_have7):
							msg_improve = "`ВСЕ ИГРОКИ ГИЛЬДИИ ЗАКОНЧИЛИ СБОР ПЕРСОНАЖА`"
						else:
							msg_improve = "_Никто больше не готов_\n"

					msg += msg_improve

					if len(not_have7_copy) > 0:
						msg += f'\nСписок тех, кто *не готов улучшить или получить*:\n_{", ".join(not_have7_copy)}_'


				# если это персонаж, которого нужно брать через ивенты - проверим готовность к ивенту
				elif pers_id in REQS:

					msg_improve = ""

					if len(not_have7) > 0: # есть игроки, у которых не на 7 звезд

						not_have7_copy = not_have7[:] # в этом листе будем держать список тех, кто остается (не сможет улучшить)

						msg += f'Кто во время следующего события сможет взять этого персонажа или улучшить по звездам'
						msg += f'\n(определяется только по нужном количеству звезд)'
						msg += ':\n\n'

						for nh in not_have7: # пробежимся по каждому игроку, у которого не на 7 звезд (nh = swgoh name) и проверим, сможет ли улучшить результат

							found_user_stat = collection_stats.find_one({"player_name": nh})
							stars = {}
							relic = {}

							for req in REQS[pers_id]: # возьмем список требований для получения и сохраним в stars значения по количеству звезд у нужных
								if req in found_user_stat:
									stars[req] = int(found_user_stat[req])
								else:
									stars[req] = 0

							# пример итога: stars["PHANTOM2"] = 7

							full_stars = []
							six_stars = []
							five_stars = []
							for key,value in stars.items(): # теперь составим список какие из них имеют 7, 6, 5 звезд
								if value == 7:
									full_stars.append(key)
									six_stars.append(key)
									five_stars.append(key)
								elif value == 6 or value == 6.0:
									six_stars.append(key)
									five_stars.append(key)
								elif value == 5 or value == 5.0:
									five_stars.append(key)


							if pers_id == "CAPITALCHIMAERA":  # особо заморочные условия получения химеры, нужно home one + ghost + phantom + еще один ребел

								base_ship_list = ["CAPITALMONCALAMARICRUISER", "GHOST", "PHANTOM2"]
								need_one_more_ship_list = ["XWINGRED3", "XWINGRED2", "UWINGROGUEONE", "UWINGSCARIF"]
								can_improve_to = 0 # по умолчанию считаем что не сможет улучшить

								### --------- проверка на 7 ------------ ####
								#############################################

								# проверим возможность получения на 7 звезд. Т.к. игрок из списка nh - значит у него точно не на 7
								for bs in base_ship_list:
									if stars[bs] == 7:
										can_improve_to = 7 # если нужный корабль на 7 звезд, то пока считаем что осилит 7
									else:
										can_improve_to = 0 # иначе все-таки пока 0 и выходим из цикла
										break

								if can_improve_to == 7: # после прохода по всем базовым кораблям пока имеем готового на 7. Проверим еще один корабль из доп списка
									
									found_one_more = False
									for nom in need_one_more_ship_list:
										if stars[nom] == 7: # нашли первый нужный корабль на 7, выходим из цикла
											found_one_more = True
											break

									if not found_one_more:
										can_improve_to = 0

								#############################################

								# на данном этапе имеем can_improve_to либо 7, либо 0

								# если все еще 0, то проверим возможность улучшения до 6 звезд, если уже не 6
								if can_improve_to == 0 and nh not in already_have6:
									
									for bs in base_ship_list:
										if stars[bs] >= 6:
											can_improve_to = 6 
										else:
											can_improve_to = 0 
											break

									if can_improve_to == 6:
										
										found_one_more = False
										for nom in need_one_more_ship_list:
											if stars[nom] >= 6: 
												found_one_more = True
												break

										if not found_one_more:
											can_improve_to = 0


								# если все еще 0, то проверим возможность улучшения до 5
								if can_improve_to == 0 and nh not in already_have6 and nh not in already_have5:
									
									for bs in base_ship_list:
										if stars[bs] >= 5:
											can_improve_to = 5 
										else:
											can_improve_to = 0 
											break

									if can_improve_to == 5:
										
										found_one_more = False
										for nom in need_one_more_ship_list:
											if stars[nom] >= 5: 
												found_one_more = True
												break
												
										if not found_one_more:
											can_improve_to = 0

								if can_improve_to == 7:
									msg_improve += f"`{nh}`: {STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}\n"
									not_have7_copy.remove(nh)
								elif can_improve_to == 6:
									msg_improve += f"`{nh}`: \u2605 \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \n"
									not_have7_copy.remove(nh)
								elif can_improve_to == 5:
									msg_improve += f"`{nh}`: \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \u2606 \n"
									not_have7_copy.remove(nh)

							elif len(full_stars)>=5: # стандартный вариант - нужно 5 любых подходящих на максимум звезд
								msg_improve += f"`{nh}`: {STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}\n"
								not_have7_copy.remove(nh)

							elif len(six_stars)>=5 and pers_id in UNLOCKS_AT_FIVE and nh not in already_have6: 
								msg_improve += f"`{nh}`: \u2605 \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \n"
								not_have7_copy.remove(nh)

							elif len(five_stars)>=5 and pers_id in UNLOCKS_AT_FIVE and nh not in already_have5 and nh not in already_have6: 
								msg_improve += f"`{nh}`: \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \u2606 \n"
								not_have7_copy.remove(nh)

							elif pers_id == "MILLENNIUMFALCON": 
								if len(full_stars) == 4:
									msg_improve += f"`{nh}`: {STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}\n"
									not_have7_copy.remove(nh)
								elif len(six_stars) == 4 and nh not in already_have6:
									msg_improve += f"`{nh}`: \u2605 \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \n"
									not_have7_copy.remove(nh)
								elif len(five_stars) == 4 and nh not in already_have5 and nh not in already_have6:
									msg_improve += f"`{nh}`: \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \u2606 \n"
									not_have7_copy.remove(nh)
								else:
									pass
									# msg_improve += f"`{nh}`: --------------\n"

							else:
								pass
								# msg_improve += f"`{nh}`: --------------\n"

					if msg_improve == "":
						if count_row == len(already_have7):
							msg_improve = "`ВСЕ ИГРОКИ ГИЛЬДИИ ЗАКОНЧИЛИ СБОР ПЕРСОНАЖА`"
						else:
							msg_improve = "_Никто больше не готов_\n"

					msg += msg_improve

					if len(not_have7_copy) > 0:
						msg += f'\nСписок тех, кто *не готов улучшить или получить*:\n_{", ".join(not_have7_copy)}_'

				bot.reply_to(message, msg, parse_mode='Markdown')
				my_logger.info("Readiness stat sent")

			else:
				bot.reply_to(message, msg_ready_help, parse_mode='Markdown')
				my_logger.info("Unknown char to check for readiness")

	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !ready: {e}")
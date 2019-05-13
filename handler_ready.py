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

				if pers_id in REQS:

					row = collection_stats.find() # соберем всю стату которая есть
					count_row = collection_stats.count_documents({}) # сколько всего игроков в базе в данный момент
					already_have7 = []
					already_have6 = []
					already_have5 = []
					not_have7 = []
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

					msg = f'(последнее обновление базы *{passed_time_text} назад*)\n\n'
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

					# в итоге в not_have7 будут все, у кого не на 7 звезд

					msg += f'Из них *{len(already_have7)}* уже имеют данного персонажа на `7` звезд:\n_{", ".join(already_have7)}_\n\n'
					if len(already_have6) > 0:
						msg += f'Еще *{len(already_have6)}* — на `6` звезд:\n_{", ".join(already_have6)}_\n\n'
					if len(already_have5) > 0:
						msg += f'И еще *{len(already_have5)}* — на `5` звезд:\n_{", ".join(already_have5)}_\n\n'
					
					# msg += f'\n'

					msg_improve = ""

					if len(not_have7) > 0:

						not_have7_copy = not_have7[:] # в этом листе будем держать список тех, кто остается (не сможет улучшить)

						msg += f'Кто во время следующего события сможет взять этого персонажа или улучшить по звездам\n'
						msg += f'(определяется только по нужном количеству звезд): \n\n'

						for nh in not_have7: # пробежимся по каждому игроку, у которого не на 7 звезд (nh = swgoh name) и проверим, сможет ли улучшить результат

							found_user_stat = collection_stats.find_one({"player_name": nh})
							stars = {}

							for req in REQS[pers_id]:
								if req in found_user_stat:
									stars[req] = found_user_stat[req]
								else:
									stars[req] = 0

							# пример итога: stars["PHANTOM2"] = 7

							full_stars = []
							six_stars = []
							five_stars = []
							for key,value in stars.items(): # теперь посчитаем сколько из них имеют 7 звезд
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

								chimaera_needs_full = []
								chimaera_needs_six = []
								chimaera_needs_five = []

								for bs in base_ship_list:
									if bs in full_stars:
										chimaera_needs_full.append(bs)
										chimaera_needs_six.append(bs)
										chimaera_needs_five.append(bs)
									elif bs in six_stars:
										chimaera_needs_six.append(bs)
										chimaera_needs_five.append(bs)
									elif bs in five_stars:
										chimaera_needs_five.append(bs)

								if len(chimaera_needs_full) == 3:
									for om in need_one_more_ship_list:
										if om in full_stars:
											msgg = f"`{nh}`: {STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}\n"
											not_have7_copy.remove(nh)
											break
										else:
											pass
											#msgg = f" --------------\n"

								elif len(chimaera_needs_six) == 3:
									for om in need_one_more_ship_list:
										if om in six_stars:
											msgg = f"`{nh}`: \u2605 \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \n"
											not_have7_copy.remove(nh)
											break
										else:
											pass
											#msgg = f" --------------\n"

								elif len(chimaera_needs_five) == 3:
									for om in need_one_more_ship_list:
										if om in five_stars:
											msgg = f"`{nh}`: \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \u2606 \n"
											not_have7_copy.remove(nh)
											break
										else:
											pass
											#msgg = f" --------------\n"

								else:
									pass
									#msgg = f" --------------\n"

								msg_improve += msgg

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
						msg += f'\nСписок тех, кто *не готов*:\n_{", ".join(not_have7_copy)}_'

					bot.reply_to(message, msg, parse_mode='Markdown')
					my_logger.info("Readiness stat sent")

				else:
					bot.reply_to(message, msg_ready_help, parse_mode='Markdown')
					my_logger.info("Unknown char to check for readiness")

			else:
				bot.reply_to(message, msg_ready_help, parse_mode='Markdown')
				my_logger.info("Unknown char to check for readiness")

	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !ready: {e}")
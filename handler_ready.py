import pymongo
from pymongo import MongoClient
import requests
import json
import time
from const import *

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_stats = mongo_db.users_stats

def handler_ready(bot,message,my_logger):

	try:

		msg_ready_help = f'Возможные варианты запросов:\n\n'
		msg_ready_help += f'`!готовность траун`\n'
		msg_ready_help += f'`!готовность c3po`\n'
		msg_ready_help += f'`!готовность рей`\n'
		msg_ready_help += f'`!готовность клюк`\n'
		msg_ready_help += f'`!готовность чубака`\n'
		msg_ready_help += f'`!готовность р2д2`\n'
		msg_ready_help += f'`!готовность бб8`\n'
		msg_ready_help += f'`!готовность палпатин`\n'
		msg_ready_help += f'`!готовность реван`\n'
		msg_ready_help += f'`!готовность сокол`\n'
		msg_ready_help += f'`!готовность химера`'

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
					count_row = collection_stats.count_documents({})
					already_have7 = []
					already_have6 = []
					already_have5 = []

					not_have = []
					msg = f'У меня есть информация о `{count_row}` игроках гильдии\n'

					for r in row: # каждая отдельная имеющаяся стата
						if pers_id in r: # искомый легендарный персонаж имеется в стате игрока
							if r[pers_id] == 7: # и у него 7 звезд
								already_have7.append(r['player_name'])
							elif r[pers_id] == 6:
								already_have6.append(r['player_name'])
								not_have.append(r['player_name'])
							elif r[pers_id] == 5:
								already_have5.append(r['player_name'])
								not_have.append(r['player_name'])
							else:
								not_have.append(r['player_name'])
						else:
							not_have.append(r['player_name'])

					msg += f'Из них `{len(already_have7)}` уже имеют данного персонажа на 7 звезд\n'
					if len(already_have6) > 0:
						msg += f'А еще `{len(already_have6)}` — на 6 звезд\n'
					if len(already_have5) > 0:
						msg += f'И еще `{len(already_have5)}` — на 5 звезд\n'
					msg += f'\n'

					if len(not_have) > 0:

						msg += f'Готовность остальных к тому, чтобы взять этого персонажа:\n'
						msg += f'(определяется только по нужном количеству звезд) \n\n'

						for nh in not_have: # пробежимся по каждому игроку, у которого нет (nh = swgoh name)

							msg += f"`{nh}`: "
							found_user_stat = collection_stats.find_one({"player_name": nh})
							stars = {}

							for req in REQS[pers_id]:
								if req in found_user_stat:
									stars[req] = found_user_stat[req]
								else:
									stars[req] = 0

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


							if pers_id == "CAPITALCHIMAERA":

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
											msgg = f" {STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI} ГОТОВ!\n"
											break
										else:
											msgg = f" --------------\n"

								elif len(chimaera_needs_six) == 3:
									for om in need_one_more_ship_list:
										if om in six_stars:
											msgg = f" *готов на* \u2605 \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \n"
											break
										else:
											msgg = f" --------------\n"

								elif len(chimaera_needs_five) == 3:
									for om in need_one_more_ship_list:
										if om in five_stars:
											msgg = f" *готов на* \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \u2606 \n"
											break
										else:
											msgg = f" --------------\n"

								else:
									msgg = f" --------------\n"

								msg += msgg

							elif len(full_stars)>=5: # для легендарного рейда нужно 5 любых персонажей на 5 звезд
								msg += f" {STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI} ГОТОВ!\n"

							elif pers_id == "MILLENNIUMFALCON":
								if len(full_stars) == 4:
									msg += f" {STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI}{STAR_EMOJI} ГОТОВ!\n"
								elif len(six_stars) == 4 and nh not in already_have6:
									msg += f" *готов на* \u2605 \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \n"
								elif len(five_stars) == 4 and nh not in already_have5:
									msg += f" *готов на* \u2605 \u2605 \u2605 \u2605 \u2605 \u2606 \u2606 \n"
								else:
									msg += f" --------------\n"

							
							else:
								msg += f" --------------\n"

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
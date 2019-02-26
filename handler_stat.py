import pymongo
from pymongo import MongoClient
import re
import requests
import json
from const import *
import time

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_stats = mongo_db.users_stats

def handler_stat(bot,message,my_logger):

	try:

		ally_code = False

		if message.text == '!stat' or message.text == '!стат': # код союзника не указан, предполагаем что игрок просит стату сам на себя
			user = message.from_user.username
			found_user = collection_users.find_one({'user': user})
			if found_user is not None:
				ally_code = found_user['ally_code']
			else:
				bot.send_message(message.chat.id, f'Пользователь {user} не зарегистрирован. Для регистрации самого себя нужно выполнить команду:\n\n`!reg кодСоюзника`\n\nТакже статистику можно запросить прямо через код союзника: \n\n`!stat кодСоюзника`', parse_mode='Markdown')
				my_logger.info(f"User {user} is not registered, can not show stat")
				return

		else: # код союзника указан в запросе
			user = message.text[6:].replace("@","")
			if re.match(r"(\D*\d){9}", user) and len(user) == 9: # вместо имени указан ally code, ну ок
				ally_code = user
			else:
				found_user = collection_users.find_one({'user': user})
				if found_user is not None:
					ally_code = found_user['ally_code']
				else:
					bot.send_message(message.chat.id, f'Пользователь {user} не зарегистрирован. Для регистрации нужно выполнить команду `!reg имяВТелеге кодСоюзника` или запросить статистику прямо через код союзника — `!stat кодСоюзника`)', parse_mode='Markdown')
					my_logger.info(f"User {user} is not registered, can not show stat")
					return

		if ally_code:

			r = requests.get(f'{SWGOH_URL}/{ally_code}/?rand={time.time()}')
			jdata = r.json()

			if jdata:
				pass
			else:
				bot.reply_to(message, f'Указанный код союзника не найден на https://swgoh.gg/p/{ally_code}/')
				my_logger.info("Ally code not found on swgoh.gg")
				return

			player_name = jdata['data']['name']
			player_gp = format(jdata['data']['galactic_power'], ',d')
			player_gp_char = format(jdata['data']['character_galactic_power'], ',d')
			player_gp_ship = format(jdata['data']['ship_galactic_power'], ',d')
			player_arena_rank = jdata['data']['arena']['rank']
			player_ship_arena_rank = jdata['data']['fleet_arena']['rank']

			player_legendaries = {}
			player_zetas = {}

			for u in jdata['units']:
				if u['data']['base_id'] is not None:  # идем по всем персонажам из статы

					# print(f"{u['data']['base_id']} - {u['data']['name']}")

					if u['data']['zeta_abilities']:
						count_zetas = len(u['data']['zeta_abilities'])
						pers_name = u['data']['name']
						player_zetas[pers_name] = count_zetas

					if u['data']['base_id'] in LEGENDARIES.keys():
						leg = u['data']['base_id']
						player_legendaries[leg] = u['data']['rarity']

			for key,value in LEGENDARIES.items():
				if key in player_legendaries.keys():
					pass
				else:
					player_legendaries[key] = 0
			
			msg = f'`{user}`\n\nИмя в SWGOH: {player_name}\nКод союзника: {ally_code}\nhttps://swgoh.gg/p/{ally_code}/\n\n'
			msg += f'Общая GP = {player_gp}\n'
			msg += f'GP персонажей = {player_gp_char}\n'
			msg += f'GP кораблей = {player_gp_ship}\n\n'

			msg += f'Арена — {player_arena_rank} место\n'
			msg += f'Арена флота — {player_ship_arena_rank} место\n\n'

			if message.chat.id == message.from_user.id:

				if len(player_legendaries):
					msg += f'Легендарные персонажи:\n\n'
					for i in range(7,-1,-1):
						for key,value in player_legendaries.items():
							if value == i:
								msg += '`'
								for x in range(1,8):
									if x <= value:
										msg += f'\u2605'
									else:
										msg += f'\u2606'
								msg += f'` {LEGENDARIES[key]}\n'

				if len(player_zetas):
					msg += f'\n Персонажи с дзетами: \n\n'
					for i in range(3,0,-1):
						for key,value in player_zetas.items():
							if value == i:
								for x in range(0,value):
									msg += f'*\u04FE*'
								msg += f' — {key}\n'
			else:
				msg += f'Более полную статистику (с легендарками и зетами) можно запросить в личке у бота @DarthBotiusBot'

			bot.send_message(message.chat.id, msg, parse_mode='Markdown', disable_web_page_preview='True')
			my_logger.info("Stat sent")

		else:
			my_logger.info("Something went wrong")

	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !stat: {e}")
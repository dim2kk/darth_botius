import pymongo
from pymongo import MongoClient
import re
import requests
import json
from const import *

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_stats = mongo_db.users_stats

def handler_reg(bot,message,my_logger):

	try:

		msg = ""
		ally_code = False
		telega_username = False
		tele_id = None

		s = message.text.split()

		if len(s) == 2:
			# передано только 1 параметр, предполагаем что это игрок регистрирует сам себя и указал ally code
			if message.from_user.username is not None: # у игрока установлен username в телеге
				if re.match(r"(\D*\d){9}", s[1]) and len(s[1]) == 9: # проверим что код = девятизначное число
					ally_code = s[1]
					telega_username = message.from_user.username
					tele_id = message.from_user.id
				else:
					bot.reply_to(message, f'Регистрация невозможна, код союзника указан неверно (правильный формат - 123456789)')
					my_logger.info("Ally code in wrong format")
					return
			else:
				bot.reply_to(message,f"Регистрация невозможна, у вас не задан username в телеграме! Задать можно в настройках приложения")
				my_logger.info("Username is None")
				return

			# на выходе имеем установленный ally_code и telega_username

		elif len(s)==3:
			# в !reg передано два параметра
			if re.match(r"(\D*\d){9}", s[2]) and len(s[2]) == 9: # проверим что код = девятизначное число
				ally_code = s[2]
				telega_username = s[1].replace("@","")
			else:
				bot.reply_to(message, f'Регистрация невозможна, код союзника указан неверно (правильный формат - 123456789)')
				my_logger.info("Ally code in wrong format")
				return

			# на выходе имеем установленный ally_code и telega_username

		else:
			bot.reply_to(message, 'Регистрация невозможна! Корректное использование:\n`!reg имяВТелеге кодСоюзника` или `!reg кодСоюзника` для регистрации себя', parse_mode="Markdown")
			my_logger.info("Registration not possible, wrong command format")


		# далее исполняется только если код союзника = девятизначное число в ally_code, а также установлен telega_username
		if ally_code and telega_username: # получим данные из swgoh.gg
			r = requests.get(f'{SWGOH_URL}/{ally_code}')
			jdata = r.json()

			if jdata:
				pass
			else:
				bot.reply_to(message, f'Регистрация невозможна, указанный код союзника не найден на https://swgoh.gg/p/{ally_code}/')
				my_logger.info("Ally code not found")
				return

			player_name = jdata['data']['name']

			# проверим, может игрок уже зарегистрирован

			found_user = collection_users.find_one({'user': telega_username})
			if found_user:
				msg = f'Пользователь {telega_username} уже зарегистрирован! '
				msg += f'Если нужно изменить информацию - сначала надо удалить пользователя через команду `!forget {telega_username}`'
				bot.send_message(message.chat.id, msg, parse_mode="Markdown")
				my_logger.info("User already exists, forget first")
			else: # регистрируем нового пользователя
				new_user = {'user': telega_username, 'ally_code': ally_code, 'swgoh_name': player_name}
				if tele_id is not None:
					new_user['tele_id'] = tele_id
				collection_users.insert_one(new_user)
				bot.send_message(message.chat.id, f'Пользователь {telega_username} успешно зарегистрирован! Найденное имя в SWGOH: {player_name}')
				my_logger.info(f"Registration successful! Found SWGOH name {player_name}")

	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !reg: {e}")
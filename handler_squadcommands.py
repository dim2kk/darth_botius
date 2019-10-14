import pymongo
import time
import math
from pymongo import MongoClient
from telebot.apihelper import ApiException
from const import *

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_users_twin = mongo_db.users_twin
collection_stats = mongo_db.users_stats
collection_squad_commands = mongo_db.squad_commands
collection_squad_commands_overview = mongo_db.squad_commands_overview

# mongo_db.users_twin
# {'user': telega_username, 'ally_code': ally_code, 'swgoh_name': swgoh_name}

# (mongo_db.squad_commands) 
#  new_squad_command = {"squad_pos": squad_pos, "squad_number": squad_number, "player_name": cur_player, "unit": cur_unit}

# squad_commands_overview
# "squad_pos": squad_pos, "squad_number": squad_number, "possibility": possibility (0=no, 1=odd, 2=ok)
# or
# "last_update": unix_timestamp, "phase": phasenumber

def get_overview():

	overview_msg = ""
	phase_number = "n/a"
	last_update = 0
	passed_time = 0
	prev_pos = '1'
	passed_time_text = "n/a"
	current_time = math.floor(time.time())

	ov_phase = collection_squad_commands_overview.find( { 'phase': { '$exists': 'true' } } )
	if ov_phase[0] is not None:
		phase_number = ov_phase[0]['phase']
		last_update = ov_phase[0]['last_update']
		passed_time = current_time-last_update

		if passed_time<60:
			passed_time_text = f"{passed_time} сек"
		elif passed_time<3600:
			passed_time_text = f"{passed_time//60} мин"
		elif passed_time<86400:
			passed_time_text = f"{passed_time//3600} ч"
		else:
			passed_time_text = "более 1 дня"

	overview_msg = f"*ФАЗА {phase_number}*\n(последнее обновление — {passed_time_text} назад)\n\n"

	ov_rows = collection_squad_commands_overview.find({ 'squad_pos': { '$exists': 'true' } }).sort([('squad_pos', pymongo.ASCENDING), ('squad_number', pymongo.ASCENDING)])
	for r in ov_rows:
		
		if r['squad_pos'] is not None:
			sp = r['squad_pos']
		if r['squad_number'] is not None:
			sn = r['squad_number']
		if r['possibility'] is not None:
			spp = r['possibility']

		if sp != prev_pos:
			overview_msg += "\n"

		if spp==0:
			overview_msg += f"❌ "
		elif spp==1:
			overview_msg += f"⚠ "
		elif spp==2:
			overview_msg += f"✅ "

		if sp=='1':
			overview_msg += f"ВЕРХ — "
		elif sp=='2':
			overview_msg += f"СЕРЕДИНА — "
		elif sp=='3':
			overview_msg += f"НИЗ — "

		overview_msg += f"{sn}\n"
		prev_pos = sp

	return overview_msg


def handler_overview_commands(bot,message,my_logger):
	try:
		overview_msg = get_overview()
		bot.send_message(message.chat.id, overview_msg, parse_mode='Markdown')

	except ApiException as e:
		my_logger.info(f'{e} while sending message')

	except Exception as e:
		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong in handler_list_commands: {e}")


def handler_list_commands(bot,message,my_logger):

	try:

		overview_msg = get_overview()
		bot.send_message(message.chat.id, overview_msg, parse_mode='Markdown')

		rows = collection_squad_commands.find().sort([('squad_pos', pymongo.ASCENDING), ('squad_number', pymongo.ASCENDING)])
		msg = ""
		cur_squad_pos_number = ""
		cur_consecutive_squads = 0

		for r in rows:

			# попробуем найти телега-айди игрока и обратиться к нему напрямую
			found_user = collection_users.find_one({"swgoh_name": r['player_name']})
			if found_user is not None:
				r['player_name'] = f"@{found_user['user']}"

			# позиции хранятся цифрами - надо переделать их в слова
			if r['squad_pos'] == "1":
				r['squad_pos'] = "ВЕРХ"
			elif r['squad_pos'] == "2":
				r['squad_pos'] = "СЕРЕДИНА"
			elif r['squad_pos'] == "3":
				r['squad_pos'] = "НИЗ"

			full_squad_pn = f"{r['squad_pos'].upper()}-{r['squad_number']}"

			if full_squad_pn != cur_squad_pos_number: # начался новый сектор в списке

				if cur_consecutive_squads == 3: # уже три взвода показано, можно начинать новое сообщение
					cur_consecutive_squads = 1
					try:
						bot.send_message(message.chat.id, msg)
					except ApiException as e:
						my_logger.info(f'{e} while sending message')
					msg = ""

				else: # надо просто добавить дополнительный перенос строки
					msg += "\n"
					cur_consecutive_squads += 1

				cur_squad_pos_number = full_squad_pn # запомним какой сектор теперь текущий

			msg += f"{full_squad_pn} — {r['player_name']} — {r['unit']}\n"

		bot.send_message(message.chat.id, msg) # отправим последнее сообщение

	except ApiException as e:
		my_logger.info(f'{e} while sending message')

	except Exception as e:
		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong in handler_list_commands: {e}")


def handler_list_commands_personal(bot,message,my_logger):

	try:

		if message.text == "!команды": # без указания, значит просит сам на себя. Попробуем узнать кто это
			username = message.from_user.username
			found_user = collection_users.find_one({"user": username})
			if found_user is not None:
				user = found_user['swgoh_name']
			else:
				bot.reply_to(message, "Нужно либо зарегистрироваться (см. `!help`), либо указать игрока, на которого запрашиваются команды (`!команды Имя В Игре`)", parse_mode='Markdown')
				return
		else:
			user = message.text.replace("!команды ", "")

		count_rows = collection_squad_commands.count_documents({"player_name": user})

		if count_rows == 0: # не нашли команд для такого игрока, а может был указан айди в телеге?
			user = user.replace("@", "")
			found_user = collection_users.find_one({"user": user})
			if found_user is not None:
				user = found_user['swgoh_name']
				count_rows = collection_squad_commands.count_documents({"player_name": user})

		if count_rows>=1: 

			rows = collection_squad_commands.find({"player_name": user})
			msg = f"*Текущий список команд по взводам для {user}:*\n\n"

			for r in rows:

				if r['squad_pos'] == "1":
					r['squad_pos'] = "ВЕРХ"
				elif r['squad_pos'] == "2":
					r['squad_pos'] = "СЕРЕДИНА"
				elif r['squad_pos'] == "3":
					r['squad_pos'] = "НИЗ"

				full_squad_pn = f"{r['squad_pos'].upper()}-{r['squad_number']}"
				msg += f"{full_squad_pn} — {r['player_name']} — {r['unit']}\n"

			if (message.from_user.id == message.chat.id): # это приват! значит можно отправлять команды 
				bot.send_message(message.chat.id, msg, parse_mode='Markdown')
			else: # не приват, а канал. Больше нельзя запрашивать команды в общем канале
				bot.reply_to(message, "Теперь `!команды` можно запросить только в привате у бота!", parse_mode='Markdown')

		else: # все равно не нашли команд, скажем что для этого игрока их нет
			if (message.from_user.id == message.chat.id): # это приват! значит можно отправлять сообщение 
				bot.send_message(message.chat.id, f'Для "{user}" не найдено команд', parse_mode='Markdown')
			else: # не приват, а канал. Больше нельзя запрашивать команды в общем канале
				bot.reply_to(message, "Теперь `!команды` можно запросить только в привате у бота!", parse_mode='Markdown')


		if message.text == "!команды": # если игрок просил сам на себя, то мы знаем его имя в телеге и можем так же проверить на команды для твинов
			
			username = message.from_user.username
			found_user = collection_users_twin.find({"user": username})
			
			if found_user is not None:

				for fu in found_user:

					twin_user = fu['swgoh_name']
					rows = collection_squad_commands.find({"player_name": twin_user})
					msg = f"*Текущий список команд по взводам для {twin_user}:*\n\n"

					for r in rows:

						if r['squad_pos'] == "1":
							r['squad_pos'] = "ВЕРХ"
						elif r['squad_pos'] == "2":
							r['squad_pos'] = "СЕРЕДИНА"
						elif r['squad_pos'] == "3":
							r['squad_pos'] = "НИЗ"

						full_squad_pn = f"{r['squad_pos'].upper()}-{r['squad_number']}"
						msg += f"{full_squad_pn} — {r['player_name']} — {r['unit']}\n"

					if (message.from_user.id == message.chat.id): # это приват! значит можно отправлять команды 
						bot.send_message(message.chat.id, msg, parse_mode='Markdown')


	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong in handler_list_commands_personal: {e}")


def handler_list_toon_usage(bot,message,my_logger):

	try:

		if message.text == "!взводы":
			bot.reply_to(message, "Нужно указать какого персонажа искать в командах на взводы.\nНапример: *!взводы Бастила Шан (Павшая)*", parse_mode='Markdown')
		
		else:

			toon = message.text.replace("!взводы ", "")
			# теперь в toon лежит типа полное название персонажа, попробуем найти его в командах взводов

			count_rows = collection_squad_commands.count_documents({"unit": toon})
			if count_rows == 0: # не найдено команд с таким персонажем
				msg = f"Не найдено использование персонажа `{toon}` в командах на взводы.\n"
				msg += f"Проверьте правильность указания персонажа.\nНапример *!взводы Бастила Шан (Павшая)*"
				bot.reply_to(message, msg, parse_mode='Markdown')

			else:

				rows = collection_squad_commands.find({"unit": toon})
				msg = f"Использование персонажа *{toon}* в командах на взводы:\n\n"

				for r in rows:

					if r['squad_pos'] == "1":
						r['squad_pos'] = "ВЕРХ"
					elif r['squad_pos'] == "2":
						r['squad_pos'] = "СЕРЕДИНА"
					elif r['squad_pos'] == "3":
						r['squad_pos'] = "НИЗ"

					full_squad_pn = f"{r['squad_pos'].upper()}-{r['squad_number']}"
					msg += f"{full_squad_pn} — {r['player_name']} — {r['unit']}\n"

				bot.reply_to(message, msg, parse_mode='Markdown')



	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong in handler_list_toon_usage: {e}")


def handler_sendall_commands(bot,message,my_logger): # не используется

	all_users = collection_stats.find()

	for user in all_users:

		# if user['player_name'] == "dim2k":

		found_user = collection_users.find_one({"swgoh_name": user['player_name']})

		if found_user is not None:
			
			tele_id = found_user['tele_id']
			if tele_id is not None:

				rows = collection_squad_commands.find({"player_name": user['player_name']})
				msg = f"*Текущий список команд по взводам для {user['player_name']}:*\n\n"

				for r in rows:

					if r['squad_pos'] == "1":
						r['squad_pos'] = "ВЕРХ"
					elif r['squad_pos'] == "2":
						r['squad_pos'] = "СЕРЕДИНА"
					elif r['squad_pos'] == "3":
						r['squad_pos'] = "НИЗ"

					full_squad_pn = f"{r['squad_pos'].upper()}-{r['squad_number']}"
					msg += f"{full_squad_pn} — {r['player_name']} — {r['unit']}\n"

					if len(msg) > 3000:
						bot.send_message(tele_id, msg, parse_mode='Markdown')
						msg = "... продолжение ... \n"

				try:
					bot.send_message(tele_id, msg, parse_mode='Markdown')
				except ApiException as ApiE:
					my_logger.info(f'{ApiE} while trying to send message to {user}')


def handler_white_check_mark(bot,message,my_logger): # не используется

	try:

		guild_players = []
		guild_chat_players = []
		cur_player = ""

		rows = collection_stats.find()
		for r in rows:
			guild_players.append(r['player_name']) # guild_players заполнено swgoh_name'ами на основе данных ги с сайта swgoh.gg

		rows = collection_users.find()
		for r in rows:
			guild_chat_players.append(r['swgoh_name']) # guild_chat_players заполнено swgoh_name'ами, зарегенными у бота

		text = message.text.split("\n")
		msg = ""

		for s in text:

			if s.startswith(':white_check_mark:') or s.startswith(':warning:'):
				s = s.replace(':white_check_mark: ', '')
				s = s.replace(':warning: ', '')
				s = s.replace('SQUADRON ', '')
				s = s.replace('PLATOON ', '')
				s = s.replace('top', '1')
				s = s.replace('mid', '2')
				s = s.replace('bottom', '3')

				ss = s.split(" - ")
				squad_number = ss[0]
				squad_pos = ss[1]

				print 

			elif s.startswith('Odd number'):
				pass

			elif s in guild_players: # это строка с ником игрока
				cur_player = s

			elif s in guild_chat_players: # может быть в guild_players нет, т.к. игрок не зареган в swgoh.gg, но зато зареган у бота (!rreg)
				cur_player = s

			else: # значит это строка с названием персонажа-корабля
				cur_unit = s
				new_squad_command = {"squad_pos": squad_pos, "squad_number": squad_number, "player_name": cur_player, "unit": cur_unit}
				collection_squad_commands.insert_one(new_squad_command)
				msg += f'Команда для `{cur_player}` разместить на *{squad_pos}-{squad_number}* юнита: _{cur_unit}_\n'

		bot.send_message(message.chat.id, msg, parse_mode='Markdown')

	except Exception as e:
		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during in handler_white_check_mark: {e}")

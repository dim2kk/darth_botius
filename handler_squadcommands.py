import pymongo
from pymongo import MongoClient
from telebot.apihelper import ApiException
from const import *

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_stats = mongo_db.users_stats
collection_squad_commands = mongo_db.squad_commands

# new_squad_command = {"squad_pos": squad_pos, "squad_number": squad_number, "player_name": cur_player, "unit": cur_unit}

def handler_white_check_mark(bot,message,my_logger):

	try:

		guild_players = []
		cur_player = ""

		rows = collection_stats.find()
		for r in rows:
			guild_players.append(r['player_name'])

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

			elif s.startswith('Odd number of possible'):
				pass

			elif s in guild_players: # это строка с ником игрока
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



def handler_list_commands(bot,message,my_logger):

	try:

		rows = collection_squad_commands.find().sort([('squad_pos', pymongo.ASCENDING), ('squad_number', pymongo.ASCENDING)])

		msg = ""
		cur_squad_pos_number = ""
		bot.send_message(message.chat.id, "*Текущий список команд по взводам:*", parse_mode='Markdown')

		for r in rows:

			# попробуем найти телега-айди игрока
			found_user = collection_users.find_one({"swgoh_name": r['player_name']})
			if found_user is not None:
				r['player_name'] = f"@{found_user['user']}"

			if r['squad_pos'] == "1":
				r['squad_pos'] = "ВЕРХ"
			elif r['squad_pos'] == "2":
				r['squad_pos'] = "СЕРЕДИНА"
			elif r['squad_pos'] == "3":
				r['squad_pos'] = "НИЗ"

			full_squad_pn = f"{r['squad_pos'].upper()}-{r['squad_number']}"
			if full_squad_pn != cur_squad_pos_number:
				msg += "\n"
				cur_squad_pos_number = full_squad_pn

			msg += f"{full_squad_pn} — {r['player_name']} — {r['unit']}\n"

			if len(msg) > 3000:
				try:
					bot.send_message(message.chat.id, msg)
				except ApiException as e:
					my_logger.info(f'{e} while sending message')
				msg = "... продолжение ... \n"

		bot.send_message(message.chat.id, msg)

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

		if count_rows == 0: # такого пользователя не нашли, а может был указан айди в телеге?
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

				if len(msg) > 3000:
					bot.send_message(message.chat.id, msg, parse_mode='Markdown')
					msg = "... продолжение ... \n"

			bot.send_message(message.chat.id, msg, parse_mode='Markdown')

		else:

			bot.send_message(message.chat.id, f'Для "{user}" не найдено команд', parse_mode='Markdown')

	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong in handler_list_commands_personal: {e}")


def handler_sendall_commands(bot,message,my_logger):

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
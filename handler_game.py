import pymongo
from pymongo import MongoClient
import time
import random
from const import *

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_current_fight = mongo_db.current_fight
collection_fights_stat = mongo_db.fights_stat

# mongo_db.users
# {'user': telega_username, 'ally_code': ally_code, 'swgoh_name': swgoh_name}

# mongo_db.current_fight
# {'id': fightid, 'f1': tgname, 'f2': tgname, 'f1_timestamp', 'f2_timestamp', 'f1_health', 'f2_health'}

# mongo_db.fights_stat
# {'f1': tgname, 'f2': tgname, 'winner': tgname, 'end_timestamp': timestamp}


def handler_arena(bot,message,my_logger):
	# просто хелп
	try: 
		msg = f'Арена Крутых Свгохеров!\n\n'
		msg += f'`!fight` - зарегистрироваться на бой\n'
		msg += f'`!attack` - атаковать, если был зарегистрирован и участвуешь в бою\n\n'
		msg += f''

		bot.send_message(message.chat.id, msg, parse_mode="Markdown")

	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong with {message.text}: {e}")


def handler_attack(bot,message,my_logger):  # атака
	try:

		username = message.from_user.username

		# сначала нужно узнать, есть ли активный бой c двумя участниками, и получить о нем инфу
		fight_is_on = False

		active_fight = collection_current_fight.find()
		if active_fight:
			if active_fight.count():
				for af in active_fight:
					af_id = af["_id"]
					if 'f1' in af and 'f2' in af: # оба игрока зарегистрированы, значит бой активен
						fight_is_on = True
						if 'next' in af:
							next = af["next"]
						else:
							next = "f1"

					else: # бой еще не начался - недостаточно зарегенных участников, не реагируем
						my_logger.info(f"Fight has not started yet (1) but {username} tries to attack")
			else:
				my_logger.info(f"Fight has not started yet (2) but {username} tries to attack")
		else:
			my_logger.info(f"Fight has not started yet (3) but {username} tries to attack")


		if fight_is_on: # бой активен!
			# данный игрок участвует в этом бою?
			#my_logger.info("Fight is on!")
			if username == af["f1"] or username == af["f2"]:
				# да, он участник!
				# а его ли это ход по очереди?
				#my_logger.info("User is a participant!")
				if username == af[next]:
					# да, наш ход!
					#my_logger.info("Yes its his turn!")
					# соберем всю нужную инфу об участниках
					opp = "f1"
					if next == "f1":
						opp = "f2"

					opp_name = af[opp]
					opp_health = af[opp+"_health"]

					next_name = af[next]
					next_health = af[next+"_health"]

					# next = "f1" or "f2"
					# opp = "f2" or "f1"
					# af_f1 and af['f1'] = some username
					# af_f2 and af['f2'] = some username
					# username = current player

					rand = random.randint(10,30)

					# бьем!
					opp_new_health = opp_health-rand
					if opp_new_health<=0:
						opp_new_health = 0

					attack_msg = f"@{next_name} нанес удар световым мечом по @{opp_name} *‒{rand}* \[{opp_new_health}/{DEFAULT_HP}]"
					bot.send_message(message.chat.id, attack_msg, parse_mode="Markdown")
					my_logger.info(f"{next_name} attacked {opp_name} dealing -{rand} damage [{opp_new_health}/{DEFAULT_HP}]")

					if opp_new_health == 0: 

						# есть победитель, завершаем бой
						msg = f"*{next_name}* побеждает! Ура!"
						bot.send_message(message.chat.id, msg, parse_mode="Markdown")
						collection_current_fight.remove({"_id": af_id})
						my_logger.info(f"Fight between {next_name} and {opp_name} ended. Winner is {next_name}")

						# запишем инфу о бое в стату					
						winner = { 'f1': next_name, 'f2': opp_name, 'winner': next_name, 'end_timestamp': time.time() }
						collection_fights_stat.insert(winner)

					else: 

						# запишем результат удара и кто следующий бьет
						collection_current_fight.update ( {'_id': af_id}, {'$set': {opp+'_health': opp_new_health, next+'_timestamp': time.time(), 'next': opp}} )
						af[opp+"_health"] = opp_new_health
						bot.send_message(message.chat.id, f"*{af['f1']}* \[{af['f1_health']}/{DEFAULT_HP}] против *{af['f2']}* \[{af['f2_health']}/{DEFAULT_HP}]\nСледующий ход за @{opp_name}", parse_mode="Markdown")
						my_logger.info(f"Fight info updated, next move is for {opp_name}")

				else:
					# ход другого игрока!
					bot.reply_to(message, f"Сейчас не ваш ход! Ждем хода от игрока *{af[next]}*", parse_mode="Markdown")
					my_logger.info(f"Wrong player to attack. Command from {username}, but next is {af[next]}")

			else:
				# неправильный игрок, никак не реагируем
				my_logger.info(f"Attacker {username} is not a participant. Fight is between {af['f1']} and {af['f2']}")



	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong with {message.text}: {e}")


def handler_fight(bot,message,my_logger):  # регистрация

	try:

		username = message.from_user.username

		# сначала нужно удостовериться, что игрок может зарегистрироваться

		# найдем активный бой
		af_id = None
		af_f1 = "[n/a]"
		af_f2 = "[n/a]"
		active_fight = collection_current_fight.find()
		if active_fight:
			if active_fight.count():
				for af in active_fight:
					af_id = af["_id"]
					if "f1" in af: # первый участник уже зареген
						af_f1 = af['f1']
						if "f2" in af: # и второй тоже - значит зарегиться больше нельзя
							af_f2 = af['f2']
							reg_pos = 0
						else: 
							reg_pos = 2
					else:
						reg_pos = 1
			else:
				reg_pos = 1
		else:
			reg_pos = 1

		# на этом этапе мы определили, может ли игрок зарегистрироваться
		# reg_pos = 0 -> не может
		# reg_pos = 1 -> записи об активном бое не найдено или почему-то первым был зареген №2
		# reg_pos = 2 -> найдена запись, где есть данные об игроке №1, значит можно зарегить последнего (второго) игрока

		if reg_pos>0:
			if af_id: # есть идентификатор записи, значит обновляем ее
				collection_current_fight.update ( {'_id': af_id}, {'$set': {"f"+str(reg_pos): username, 'f'+str(reg_pos)+'_timestamp': time.time(), 'f'+str(reg_pos)+'_health': DEFAULT_HP}} )
			else: # создаем новую запись
				new_fight = {'f'+str(reg_pos): username, 'f'+str(reg_pos)+'_timestamp': time.time(), 'f'+str(reg_pos)+'_health': DEFAULT_HP}
				collection_current_fight.insert(new_fight)

			bot.reply_to(message, f'Регистрация игрока *{username}* успешна!', parse_mode="Markdown")
			my_logger.info(f"Success registering {username} for a fight")

			active_fight = collection_current_fight.find()
			if active_fight.count():
				for af in active_fight:
					if 'f1' in af and 'f2' in af: # оба игрока зарегистрированы
						bot.send_message(message.chat.id, f"Начинается бой между {af['f1']} и {af['f2']}!\nПервый ход за игроком №1 - *{af['f1']}*", parse_mode="Markdown")
						collection_current_fight.update ( {"_id": af_id}, {"$set": {"next": "f1"}} )

		else:
			bot.reply_to(message, f'Невозможно зарегистрироваться, уже идет бой между *{af_f1}* и *{af_f2}*!', parse_mode="Markdown")
			my_logger.info(f"Can't register {username} cos a fight is on between {af_f1} и {af_f2}!")


	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!", parse_mode="Markdown")
		my_logger.info(f"Something went wrong during !reg: {e}")


def handler_cancelfight(bot,message,my_logger):  # отмена текущего боя

	try:

		# найдем активный бой
		af_id = None
		active_fight = collection_current_fight.find()
		if active_fight:
			if active_fight.count(): # найден
				for af in active_fight:
					af_id = af["_id"]
					collection_current_fight.remove({"_id": af_id})
					bot.reply_to(message, f"Отменен активный бой между {af['f1']} и {af['f1']}")
					my_logger.info(f"Canceled fight between {af['f1']} и {af['f1']}")

			else:
				bot.reply_to(message, f"Не найден бой для отмены")
				my_logger.info(f"Can't cancel fight - no fight found")
		else:
			bot.reply_to(message, f"Не найден бой для отмены")
			my_logger.info(f"Can't cancel fight - no fight found")

	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !reg: {e}")




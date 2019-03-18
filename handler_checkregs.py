import pymongo
from pymongo import MongoClient

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_stats = mongo_db.users_stats

def handler_checkregs(bot,message,my_logger):

	try:

		bot_list = collection_users.find() # список зарегенных у бота
		swgohgg_list = collection_stats.find() # состав ги по данным swgoh.gg, спарсенным ранее командой !up

		# сначала проверим кто из игроков по данным сайта не зареген у бота
		msg = "Список игроков по данным swgoh.gg, которые не зарегистрированы у бота:\n\n"
		for sl in swgohgg_list:
			name = sl['player_name']
			found_user = collection_users.find_one({"swgoh_name": name})
			if found_user is not None:
				# все ок, этот зареген
				pass
			else:
				msg += f"{name} ({sl['ally_code']})\n"

		bot.send_message(message.chat.id, msg)

		# а теперь кто зареген у бота, но отсутствует на сайте
		msg = "Список игроков, зарегистрированных у бота, но отсутствующих в гильдии по данным сайта swgoh.gg:\n\n"
		for bl in bot_list:
			name = bl['swgoh_name']
			found_user = collection_stats.find_one({"player_name": name})
			if found_user is not None:
				# все ок, этот зареген
				pass
			else:
				msg += f"{name} ({bl['ally_code']}, @{bl['user']})\n"

		bot.send_message(message.chat.id, msg)

		my_logger.info(f"Sent info !checkregs")

	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !checkregs: {e}")
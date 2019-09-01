import pymongo
from pymongo import MongoClient
from const import *

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_users_twin = mongo_db.users_twin
collection_stats = mongo_db.users_stats

# mongo_db.users
# {'user': telega_username, 'ally_code': ally_code, 'swgoh_name': swgoh_name}

# mongo_db.users_twin
# {'user': telega_username, 'ally_code': ally_code, 'swgoh_name': swgoh_name}

def handler_list(bot,message,my_logger):

	try:

		row = collection_users.find().sort([('swgoh_name', pymongo.ASCENDING)])
		count_row = collection_users.count_documents({})
		msg = 'Список всех зарегистрированных пользователей:\n\n'
		for r in row:
			msg += f"{r['swgoh_name']} - @{r['user']} [{r['ally_code']}]"
			if message.chat.id == OWNER and 'tele_id' in r.keys():
				msg += f" [tg {r['tele_id']}]"
			msg += "\n"

		if message.from_user.id!=message.chat.id:
			bot.reply_to(message, "Список можно запросить только в личке с ботом")
			bot.send_message(message.from_user.id, msg)
		else:
			bot.send_message(message.chat.id, msg)

		if message.chat.id in ADMINS:
			# дополнительно отправим список твинов, если это приват с админом
			row = collection_users_twin.find().sort([('user', pymongo.DESCENDING)])
			msg = 'Список твинов:\n\n'
			for r in row:
				msg += f"{r['swgoh_name']} - @{r['user']} [{r['ally_code']}]\n"

			bot.send_message(message.chat.id, msg)

		my_logger.info("List sent")

	except Exception as e:
		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !reg: {e}")
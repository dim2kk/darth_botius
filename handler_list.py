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

		row = collection_users.find().sort([('is_admin', pymongo.DESCENDING), ('tele_id', pymongo.DESCENDING)])
		count_row = collection_users.count_documents({})
		msg = 'Список всех зарегистрированных пользователей:\n\n'
		for r in row:
			if message.chat.id == OWNER and 'tele_id' in r.keys():
				msg += "☞ "
			if message.chat.id == OWNER and 'is_admin' in r.keys():
			 	msg += f"{STAR_EMOJI} "
			msg += f"{r['user']}"
			if message.chat.id == OWNER and 'tele_id' in r.keys():
				msg += f" [id{r['tele_id']}]"
			msg += f" ({r['swgoh_name']} - {r['ally_code']})\n"

		if count_row>35 and message.from_user.id!=message.chat.id:
			bot.reply_to(message, "Список слишком длинный, отправил в личку")
			bot.send_message(message.from_user.id, msg)
		else:
			bot.send_message(message.chat.id, msg)

		if message.chat.id in ADMINS:
			# дополнительно отправим список твинов, если это приват с админом
			row = collection_users_twin.find().sort([('user', pymongo.DESCENDING)])
			msg = 'Список твинов:\n\n'
			for r in row:
				msg += f"{r['user']} ({r['swgoh_name']} - {r['ally_code']})\n"

			bot.send_message(message.chat.id, msg)

		my_logger.info("List sent")

	except Exception as e:
		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !reg: {e}")
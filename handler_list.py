import pymongo
from pymongo import MongoClient
from const import *

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_stats = mongo_db.users_stats

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
		my_logger.info("List sent")

	except Exception as e:
		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !reg: {e}")
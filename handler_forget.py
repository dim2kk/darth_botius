import pymongo
from pymongo import MongoClient

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_stats = mongo_db.users_stats

def handler_forget(bot,message,my_logger):

	try:

		if message.text == '!forget' or message.text == '!забыть': # код союзника не указан, предполагаем что игрок удаляет сам себя
			user = message.from_user.username
		else:
			user = message.text[8:].replace("@","")

		if user:
			found_user = collection_users.find_one({'user': user})
			if found_user is not None:
				collection_users.delete_one({"_id": found_user['_id']})
				bot.reply_to(message, f'Пользователь {user} удален из базы')
				my_logger.info(f'User {user} deleted')
			else:
				bot.reply_to(message, f'Пользователь {user} не найден!!!')
				my_logger.info(f'User {user} not found')

	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !forget: {e}")
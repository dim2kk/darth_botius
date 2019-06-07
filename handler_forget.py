import pymongo
from pymongo import MongoClient

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_users_twin = mongo_db.users_twin
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


def handler_twin_forget(bot,message,my_logger):

	try:

		if message.text == '!twinforget': # не указано кого удалять
			bot.reply_to(message, 'Удаление твина невозможно! Корректное использование:\n`!twinforget username', parse_mode="Markdown")
			my_logger.info("Twin delete not possible, wrong command format")
		else:
			user = message.text[12:].replace("@","")

		if user:
			found_user = collection_users_twin.find_one({'user': user})
			if found_user is not None:
				collection_users_twin.delete_one({"_id": found_user['_id']})
				bot.reply_to(message, f'Твин пользователя {user} c игровым именем {found_user["swgoh_name"]} удален из базы')
				my_logger.info(f'Twin user {user} deleted')
			else:
				bot.reply_to(message, f'У пользователя {user} не найдены твины!')
				my_logger.info(f'Twins for user {user} not found')

	except Exception as e:

		bot.reply_to(message, "Произошла ошибка, попробуйте позже!")
		my_logger.info(f"Something went wrong during !forget: {e}")
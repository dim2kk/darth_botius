#!/home/dima/telegram_bots/darth/bin/python3
# -*- coding: utf-8 -*-

# https://github.com/eternnoir/pyTelegramBotAPI

# mongo_db.users
# {'user': telega_username, 'ally_code': ally_code, 'swgoh_name': swgoh_name}

# mongo_db.users_stats (!up)
# {"player_name": swgoh_name, "ally_code": ally_code, "last_update": time.time(), [unit_id]: [unit_rarity]}

# mongo_db.squad_commands
# {"squad_pos": squad_pos, "squad_number": squad_number, "player_name": swgoh_name, "unit": unit_name_rus}

import random 
import telebot
from telebot.types import Message
from telebot.apihelper import ApiException
import telebot.types
import requests
import json
import re
import logging
import logging.handlers
import pymongo
import time
from pymongo import MongoClient

import ssl
from aiohttp import web

from const_secured import *  # TOKEN, LOG_FILE_PATH, WEBHOOK_HOST, WEBHOOK_PORT, etc.
from const import *
from handler_forget import *
from handler_reg import *
from handler_stat import *
from handler_up import *
from handler_list import *
from handler_ready import *
from handler_squadcommands import *
from handler_checkregs import *

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(TOKEN)

app = web.Application()

# Process webhook calls
async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

app.router.add_post('/{token}/', handle)

format_str = '%(asctime)s %(message)s'
date_format = '%d.%m.%Y %H:%M:%S'

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.INFO)
fh = logging.handlers.RotatingFileHandler(LOG_FILE_PATH, maxBytes=50000, backupCount=100)
formatter = logging.Formatter(format_str, date_format)
fh.setFormatter(formatter)
my_logger.addHandler(fh)

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_stats = mongo_db.users_stats
collection_squad_commands = mongo_db.squad_commands

bot = telebot.TeleBot(TOKEN)

bot.send_message(OWNER, "Start successful!")

@bot.message_handler(commands=['start', 'help'])
def command_handler(message: Message):
	bot.send_message(message.chat.id, help_msg, parse_mode="Markdown")
	if message.from_user.id == message.chat.id and message.from_user.id in ADMINS: # это приват с админом!
		bot.send_message(message.chat.id, extra_help_msg, parse_mode="Markdown")


@bot.message_handler(commands=['commands'])
def command_handler(message: Message):
	message.text = "!команды"
	handler_list_commands_personal(bot,message,my_logger)


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def handle_text(message: Message):

	if message.text.startswith('!'):

		if message.chat.type=="private":
			chat_name = f"private chat"
		else:
			chat_name = message.chat.title

		my_logger.info(f'Command issued: "{message.text}" by {message.from_user.username} in {chat_name}')

		if message.text.lower() == "!help" or message.text.lower() == "!помощь":
			bot.send_message(message.chat.id, help_msg, parse_mode="Markdown")
			if message.from_user.id == message.chat.id and message.from_user.id in ADMINS: # это приват с админом!
				bot.send_message(message.chat.id, extra_help_msg, parse_mode="Markdown")

		elif message.text.startswith('!reg') or message.text.startswith('!рег'): # возможные варианты: !reg code, !reg name code
			handler_reg(bot,message,my_logger)

		elif (message.text.startswith('!rreg') or message.text.startswith('!ррег')) and message.from_user.id in ADMINS: # вариация для администратора
			handler_reg(bot,message,my_logger)
			
		elif (message.text.startswith('!forget') or message.text.startswith('!забыть')) and message.from_user.id in ADMINS:
			handler_forget(bot,message,my_logger)

		elif message.text.startswith('!promote') and message.from_user.id == OWNER:
			user = message.text[9:].replace("@","")
			found_user = collection_users.find_one({'user': user})
			if found_user is not None:
				collection_users.update ( {'_id': found_user['_id']}, {'$set': {'is_admin': 1}} )
				bot.reply_to(message, f"Пользователь {user} теперь администратор!")
				my_logger.info(f"User {user} has been promoted!")
			else:
				bot.reply_to(message, f"Пользователь {user} не найден в списке зарегистрированных")
				my_logger.info(f"User {user} not found!")

		elif message.text.startswith('!demote') and message.from_user.id == OWNER:
			user = message.text[8:].replace("@","")
			found_user = collection_users.find_one({'user': user})
			if found_user is not None:
				collection_users.update ( {'_id': found_user['_id']}, {'$unset': {'is_admin': 1}} )
				bot.reply_to(message, f"Пользователь {user} больше не администратор!")
				my_logger.info(f"User {user} has been demoted!")
			else:
				bot.reply_to(message, f"Пользователь {user} не найден в списке зарегистрированных")
				my_logger.info(f"User {user} not found!")

		elif message.text.startswith('!stat') or message.text.startswith('!стат'):
			handler_stat(bot,message,my_logger)
			
		elif (message.text == '!list' or message.text == '!лист' or message.text == '!список') and message.from_user.id in ADMINS:
			handler_list(bot,message,my_logger)

		elif (message.text.startswith('!up') or message.text.startswith('!ап')) and message.from_user.id in ADMINS:
			handler_up(bot,message,my_logger)

		elif message.text.startswith('!готовность'):
			handler_ready(bot,message,my_logger)

		elif message.text.startswith('!clearcommands') and message.from_user.id in ADMINS:
			collection_squad_commands.delete_many({})
			bot.reply_to(message, f"Список очищен!")

		elif message.text.startswith('!listcommands') and message.from_user.id in ADMINS:
			handler_list_commands(bot,message,my_logger)

		elif message.text.startswith('!tboverview') and message.from_user.id in ADMINS:
			handler_overview_commands(bot,message,my_logger)

		elif message.text.startswith('!sendallcommands') and message.from_user.id in ADMINS:
			handler_sendall_commands(bot,message,my_logger)

		elif message.text.startswith('!checkregs') and message.from_user.id in ADMINS:
			handler_checkregs(bot,message,my_logger)

		elif message.text.startswith('!команды'):
			handler_list_commands_personal(bot,message,my_logger)

			
		else:
			print(f'Unidentified command in message: {message.text}')

	
	# elif message.text.startswith(':white_check_mark:') or message.text.startswith(':warning:'):
	# 	handler_white_check_mark(bot,message,my_logger)


	else: # просто все сообщения в чате - сохраним инфу о чатайди для зарегистрированных, ибо надо
		username = message.from_user.username
		userid = message.from_user.id

		found_user = collection_users.find_one({'user': username})
		if found_user is not None:
			if 'tele_id' in found_user.keys():
				pass
			else:
				collection_users.update ( {'_id': found_user['_id']}, {'$set': {'tele_id': userid}} )
				print(f'tele_id saved for {username}')
				my_logger.info(f"tele_id saved for {username}")


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Build ssl context
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

# Start aiohttp server
web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)
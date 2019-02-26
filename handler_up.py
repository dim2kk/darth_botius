import pymongo
from pymongo import MongoClient
import requests
import json
import time
from const import *

mongo_client = MongoClient()
mongo_db = mongo_client.darth
collection_users = mongo_db.users
collection_stats = mongo_db.users_stats

def handler_up(bot,message,my_logger):

	bot.send_message(message.chat.id, "Updating!")

	collection_stats.delete_many({}) # очистили коллекцию со статой

	try:

		req = requests.get(f"{SWGOH_GUILD_URL}/?rand={time.time()}")
		jdata = req.json()

		for j_player in jdata['players']:

			player_name = j_player['data']['name']
			player_ally_code = j_player['data']['ally_code']

			new_stat = {"player_name": player_name, "ally_code": player_ally_code, "last_update": time.time()}

			for j_unit in j_player['units']: # идем по всем юнитам игрока
				unit_id = j_unit['data']['base_id']
				unit_rarity = j_unit['data']['rarity']
				# unit_gear_level = j_unit['data']['gear_level']
				# unit_pretty_name = j_unit['data']['name']
				new_stat[unit_id] = unit_rarity
				# new_stat[f'{unit_id}_gear'] = unit_gear_level

			collection_stats.insert_one(new_stat)
			print (f'inserted {player_name}')

	except Exception as e:
		bot.send_message(message.chat.id, "Something went wrong!")
		my_logger.info(f"Something went wrong: {e}")

	else:
		bot.send_message(message.chat.id, "Update complete!")
		my_logger.info("Update complete")
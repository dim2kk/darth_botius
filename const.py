SWGOH_URL = 'https://swgoh.gg/api/player'
SWGOH_GUILD_URL = 'https://swgoh.gg/api/guild/30876'
ADMINS = [48839336, 504507571, 326656067, 238761218]  # я, морт, гном, анадерон
OWNER = 48839336 # dim2k
STAR_EMOJI = '⭐'

LEGENDARIES = { 
				"GRANDADMIRALTHRAWN": "Grand Admiral Thrawn", 
				"REYJEDITRAINING": "Jedi Training Rey",
				"COMMANDERLUKESKYWALKER": "Commander Luke Skywaker",
				"R2D2_LEGENDARY": "R2-D2",
				"BB8": "BB8",
				"EMPERORPALPATINE": "Emperor Palpatine",
				"GRANDMASTERYODA": "Grand Master Yoda",
				"DARTHTRAYA": "Darth Traya",
				"C3POLEGENDARY": "C3PO",
				"CHEWBACCALEGENDARY": "Chewbacca",
				"JEDIKNIGHTREVAN": "Jedi Knight Revan",
				"HERMITYODA": "Hermit Yoda",
				"WAMPA": "Wampa"
			  }

REQS = {}

REQS['GRANDADMIRALTHRAWN'] = ["EZRABRIDGERS3", "HERASYNDULLAS3", "KANANJARRUSS3", "ZEBS3", "CHOPPERS3", "SABINEWRENS3"]
REQS['REYJEDITRAINING'] = ["REY", "FINN", "BB8", "SMUGGLERHAN", "SMUGGLERCHEWBACCA"]
REQS['COMMANDERLUKESKYWALKER'] = ["LUKESKYWALKER", "PRINCESSLEIA", "R2D2_LEGENDARY", "STORMTROOPERHAN", "OLDBENKENOBI"]

REQS['R2D2_LEGENDARY'] = ["GRANDADMIRALTHRAWN", "EMPERORPALPATINE", "VADER", "DEATHTROOPER", "TIEFIGHTERPILOT", 
							"GRANDMOFFTARKIN", "SNOWTROOPER", "MAGMATROOPER", "STORMTROOPER", "VEERS", 
							"COLONELSTARCK", "ROYALGUARD", "GARSAXON", "IMPERIALPROBEDROID", "RANGETROOPER", "SHORETROOPER", 
							"IMPERIALSUPERCOMMANDO", "DIRECTORKRENNIC"]

REQS['BB8'] = ["PHASMA", "FIRSTORDEREXECUTIONER", "FIRSTORDEROFFICERMALE", "FIRSTORDERSPECIALFORCESPILOT", "FIRSTORDERTROOPER", 
							"FIRSTORDERTIEPILOT", "KYLOREN", "KYLORENUNMASKED"]

REQS['EMPERORPALPATINE'] = ["ADMIRALACKBAR", "FULCRUMAHSOKA", "BAZEMALBUS", "BIGGSDARKLIGHTER", "BISTAN", 
							"BODHIROOK", "C3POLEGENDARY", "HOTHHAN", "CASSIANANDOR", "CHEWBACCALEGENDARY", 
							"CHIRRUTIMWE", "CHOPPERS3", "COMMANDERLUKESKYWALKER", "EZRABRIDGERS3", "ZEBS3", 
							"HERASYNDULLAS3", "HANSOLO", "HOTHREBELSCOUT", "JYNERSO", "K2SO",
							"KANANJARRUSS3", "ADMINISTRATORLANDO", "LOBOT", "LUKESKYWALKER", "OLDBENKENOBI",
							"PAO", "PRINCESSLEIA", "R2D2_LEGENDARY", "HOTHLEIA", "SABINEWRENS3",
							"SCARIFREBEL", "STORMTROOPERHAN", "WEDGEANTILLES"]

REQS['GRANDMASTERYODA'] = ["AAYLASECURA", "AHSOKATANO", "BARRISSOFFEE", "BASTILASHAN", "EETHKOTH", 
							"EZRABRIDGERS3", "GENERALKENOBI", "HERMITYODA", "IMAGUNDI", "JEDIKNIGHTCONSULAR",
							"ANAKINKNIGHT", "JEDIKNIGHTGUARDIAN", "JEDIKNIGHTREVAN", "JOLEEBINDO", "JUHANI",
							"KANANJARRUSS3", "KITFISTO", "LUMINARAUNDULI", "MACEWINDU", "OLDBENKENOBI",
							"PLOKOON", "QUIGONJINN"]

REQS['CHEWBACCALEGENDARY'] = ["AURRA_SING", "BOBAFETT", "BOSSK", "CADBANE", "DENGAR", 
							"EMBO", "GREEDO", "IG88", "JANGOFETT", "ZAMWESELL"]

REQS['C3POLEGENDARY'] = ["CHIEFCHIRPA", "EWOKELDER", "EWOKSCOUT", "LOGRAY", "PAPLOO", "TEEBO", "WICKET"]
REQS['JEDIKNIGHTREVAN'] = ["BASTILASHAN", "JOLEEBINDO", "T3_M4", "MISSIONVAO", "ZAALBAR"]

REQS['MILLENNIUMFALCON'] = ["HOUNDSTOOTH", "IG2000", "SLAVE1", "XANADUBLOOD"]

REQS['CAPITALCHIMAERA'] = ["CAPITALMONCALAMARICRUISER", "GHOST", "PHANTOM2", "XWINGRED3", "XWINGRED2", "UWINGROGUEONE", "UWINGSCARIF"]

UNLOCKS_AT_FIVE = ["MILLENNIUMFALCON", "R2D2_LEGENDARY", "BB8", "GRANDADMIRALTHRAWN", "C3POLEGENDARY",
					"CHEWBACCALEGENDARY", "CAPITALCHIMAERA"]

REQS_ALIASES = {

	'c3po': "C3POLEGENDARY",
	'ситрипио': "C3POLEGENDARY",
	'с3ро': "C3POLEGENDARY",

	'йода': "GRANDMASTERYODA",
	'gmy': "GRANDMASTERYODA",
	'гмй': "GRANDMASTERYODA",

	'чубакка': "CHEWBACCALEGENDARY",
	'чубака': "CHEWBACCALEGENDARY",
	'чуи': "CHEWBACCALEGENDARY",
	'chewbacca': "CHEWBACCALEGENDARY",
	'chewbaca': "CHEWBACCALEGENDARY",
	'собака': "CHEWBACCALEGENDARY",

	'rey': "REYJEDITRAINING", 
	'jtr': "REYJEDITRAINING",
	'рей': "REYJEDITRAINING",
	'рэй': "REYJEDITRAINING",
	'рсм': "REYJEDITRAINING",

	'реван': "JEDIKNIGHTREVAN", 
	'revan': "JEDIKNIGHTREVAN",
	'jkr': "JEDIKNIGHTREVAN",

	'клюк': "COMMANDERLUKESKYWALKER",
	'люк': "COMMANDERLUKESKYWALKER",
	'luke': "COMMANDERLUKESKYWALKER",

	'r2d2': "R2D2_LEGENDARY",
	'р2д2': "R2D2_LEGENDARY",

	'bb8': "BB8",
	'бб8': "BB8",

	'палпатин': "EMPERORPALPATINE",
	'palpatine': "EMPERORPALPATINE",
	'palpatin': "EMPERORPALPATINE",

	'сокол': "MILLENNIUMFALCON",
	'falcon': "MILLENNIUMFALCON",

	'химера': "CAPITALCHIMAERA",
	'chimaera': "CAPITALCHIMAERA",

	'thrawn': "GRANDADMIRALTHRAWN",
	'траун': "GRANDADMIRALTHRAWN"
}


help_msg = f'Список возможных команд:\n\n'
help_msg += '`!reg` или `!рег` — регистрация нового игрока у бота. Нужна для того, чтобы можно было запрашивать статистику по !stat имяВТелеге\nВарианты использования:\n'
help_msg += '`!reg кодСоюзника` = зарегистрировать себя с указанным кодом союзника\n'
help_msg += '`!reg имяВТелеге кодСоюзника` = зарегистрировать указанного пользователя телеграмма с указанным кодом союзника\n'
help_msg += 'Код союзника указывается в формате 123456789\n\n'
help_msg += '`!list` или `!список`\nСписок всех игроков, зарегистрированных у бота\n\n'
help_msg += '`!forget имяВТелеге`\nОтменить регистрацию игрока с указанным username\nМожно использовать просто `!forget` чтобы отменить свою регистрацию\n\n'
help_msg += '`!stat имяВТелеге` или `!стат имяВТелеге`\n'
help_msg += 'Вывод статистики GP и арены по зарегистрированному игроку с указанным именем в телеге.\n'
help_msg += 'Также возможен вариант `!stat кодСоюзника` для незарегистрированных игроков\n'
help_msg += 'Или просто `!stat` для запроса на себя (если ранее была регистрация)\n\n'

help_msg += '`!команды` или `!команды никВИгре`\n'
help_msg += 'Вывод текущих команд на взводы на себя или на указанного игрока.\n'
help_msg += 'Для данной команды нужно указать именно ник в игре. Можно попробовать ник в телеграме, но только если он зарегистрирован у бота\n'
help_msg += 'На себя (просто `!команды`) тоже сработает только если есть регистрация\n\n'

help_msg += 'Команды можно отправлять в личку боту, либо прямо в канале.\n\n'
help_msg += '`имяВТелеге` — *это username, который используется для обращения к пользователю* (не Имя-Фамилия, не ник).'
help_msg += 'Его нужно задать в настройках Телеграма. Боту можно передавать username с символом @ или без него'

extra_help_msg = f'Дополнительные команды для администраторов:\n\n'
extra_help_msg += '`!clearcommands` — очистить текущий список команд для взводов. Нужно сделать перед тем, как добавлять новые команды\n\n'
extra_help_msg += 'После очистки можно по одному сектору отправлять боту список команд, скопированных от бота из discord\n\n'
extra_help_msg += '`!listcommands` — вывести полный список всех сохраненных команд (очень много текста)\n\n'
extra_help_msg += '`!sendallcommands` — разослать в личку зарегистрированным пользователям их персональные команды\n\n'

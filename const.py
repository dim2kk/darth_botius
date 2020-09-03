SWGOH_URL = 'https://swgoh.gg/api/player'
SWGOH_GUILD_URL = 'https://swgoh.gg/api/guild/30876'
STAR_EMOJI = '⭐'

FIGHT_TIMEOUT = 300 # 5 мин таймаут на реакцию
DEFAULT_HP = 100

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
				"DARTHREVAN": "Darth Revan",
				"PADMEAMIDALA": "Padme Amidala",
				"HERMITYODA": "Hermit Yoda",
				"WAMPA": "Wampa",
				"DARTHTRAYA": "Darth Traya",
				"GENERALSKYWALKER": "General Skywalker",
				"JEDIKNIGHTLUKE": "Jedi Knight Luke Skywalker",
				"GLREY": "Galactic Legend Rey",
				"SUPREMELEADERKYLOREN": "Supreme Leader Kylo Ren",
				"KIADIMUNDI": "Ki Adi Mundi",
				"WATTAMBOR": "Wat Tambor"
			  }

REQS = {}
REQS_LONG = {}

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

REQS['DARTHREVAN'] = ["BASTILASHANDARK", "CANDEROUSORDO", "CARTHONASI", "HK47", "JUHANI"]

REQS['JEDIKNIGHTREVAN'] = ["BASTILASHAN", "JOLEEBINDO", "T3_M4", "MISSIONVAO", "ZAALBAR"]

REQS['PADMEAMIDALA'] = ["ASAJVENTRESS", "GEONOSIANSOLDIER", "GEONOSIANSPY", "NUTEGUNRAY", "POGGLETHELESSER", "MAGNAGUARD", 
						"GRIEVOUS", "SUNFAC", "B1BATTLEDROIDV2", "COUNTDOOKU", "DROIDEKA", "B2SUPERBATTLEDROID", "GEONOSIANBROODALPHA"]

REQS['MILLENNIUMFALCON'] = ["HOUNDSTOOTH", "IG2000", "SLAVE1", "XANADUBLOOD"]

REQS['CAPITALCHIMAERA'] = ["CAPITALMONCALAMARICRUISER", "GHOST", "PHANTOM2", "XWINGRED3", "XWINGRED2", "UWINGROGUEONE", "UWINGSCARIF"]

LIST_WITH_LONG_REQS = ["GENERALSKYWALKER", "JEDIKNIGHTLUKE", "GLREY", "SUPREMELEADERKYLOREN", "WATTAMBOR", "KIADIMUNDI"]

REQS_LONG["KIADIMUNDI"] = {   "SHAAKTI": "gear 18", 
							 "CT7567": "gear 18",   # rex
							 "CT5555": "gear 20", 
							 "CT210408": "gear 20",  #echo
							 "ARCTROOPER501ST": "gear 20" }

REQS_LONG["WATTAMBOR"] = {   "GEONOSIANSOLDIER": "gear 12", 
							 "GEONOSIANSPY": "gear 12",   
							 "POGGLETHELESSER": "gear 12", 
							 "SUNFAC": "gear 12",  
							 "GEONOSIANBROODALPHA": "gear 12" }

REQS_LONG["GENERALSKYWALKER"] = { 	
									#"CAPITALJEDICRUISER": "power 40000", 
							 		#"JEDISTARFIGHTERANAKIN": "power 40000", 
							 		#"JEDISTARFIGHTERAHSOKATANO": "power 40000", 
							 		#"BLADEOFDORIN": "power 40000", 
							 		#"ARC170CLONESERGEANT": "power 40000", 
									"AHSOKATANO": "power 17700", 
							 		"C3POLEGENDARY": "power 17700", 
							 		"GENERALKENOBI": "power 17700", 
							 		"PADMEAMIDALA": "power 17700", 
							 		"SHAAKTI": "power 17700", 
							 		"ASAJVENTRESS": "power 17700", 
							 		"B1BATTLEDROIDV2": "power 17700", 
							 		"B2SUPERBATTLEDROID": "power 17700",
							 		"DROIDEKA": "power 17700", 
							 		"MAGNAGUARD": "power 17700" }

REQS_LONG["JEDIKNIGHTLUKE"] = { "C3POLEGENDARY": "gear 16", 
							 "VADER": "gear 16", 
							 "WAMPA": "gear 16", 
							 "CHEWBACCALEGENDARY": "gear 16", 
							 "HOTHLEIA": "gear 16", 
							 "HOTHHAN": "gear 16", 
							 "ADMINISTRATORLANDO": "gear 16", 
							 "HERMITYODA": "gear 16", 
							 "COMMANDERLUKESKYWALKER": "gear 16" }

REQS_LONG["GLREY"] = { "AMILYNHOLDO": "gear 18",
					"BB8": "gear 20",
					"FINN": "gear 18",
					"POE": "gear 18",
					"EPIXFINN": "gear 18",
					"EPIXPOE": "gear 18",
					"RESISTANCEPILOT": "gear 16",
					"RESISTANCETROOPER": "gear 18",
					"REYJEDITRAINING": "gear 20",
					"REY": "gear 20",
					"ROSETICO": "gear 18",
					"SMUGGLERCHEWBACCA": "gear 16",
					"CAPITALRADDUS": "stars 5" }

REQS_LONG["SUPREMELEADERKYLOREN"] = { 	"KYLORENUNMASKED": "gear 20",
								   	"FIRSTORDERTROOPER": "gear 18",
								   	"FIRSTORDEROFFICERMALE": "gear 18",
									"KYLOREN": "gear 20",
									"PHASMA": "gear 18",
									"FIRSTORDEREXECUTIONER": "gear 18",
									"SMUGGLERHAN": "gear 16",
									"FOSITHTROOPER": "gear 18",
									"TIEFIGHTERFOSF": "gear 16",
									"GENERALHUX": "gear 18",
									"FIRSTORDERTIEPILOT": "gear 16",
									"EMPERORPALPATINE": "gear 20",
									"CAPITALFINALIZER": "stars 5" }


UNLOCKS_AT_FIVE = ["MILLENNIUMFALCON", "R2D2_LEGENDARY", "BB8", "GRANDADMIRALTHRAWN", "C3POLEGENDARY",
					"CHEWBACCALEGENDARY", "CAPITALCHIMAERA", "PADMEAMIDALA"]

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
	'реванка': "JEDIKNIGHTREVAN",
	'revan': "JEDIKNIGHTREVAN",
	'jkr': "JEDIKNIGHTREVAN",

	'древан': "DARTHREVAN",
	'древанка': "DARTHREVAN",
	'дартреван': "DARTHREVAN",
	'darthrevan': "DARTHREVAN",
	'drevan': "DARTHREVAN",

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

	'падме': "PADMEAMIDALA",
	'падла': "PADMEAMIDALA",
	'padme': "PADMEAMIDALA",
	'amidala': "PADMEAMIDALA",
	'амидала': "PADMEAMIDALA",

	'хермит': "HERMITYODA",
	'hermit': "HERMITYODA",
	'хода': "HERMITYODA",
	'hoda': "HERMITYODA",
	'отшельник': "HERMITYODA",

	'вампа': "WAMPA",
	'wampa': "WAMPA",

	'трея': "DARTHTRAYA",
	'traya': "DARTHTRAYA",

	'thrawn': "GRANDADMIRALTHRAWN",
	'траун': "GRANDADMIRALTHRAWN",

	'гэс': "GENERALSKYWALKER",
	'gas': "GENERALSKYWALKER",

	'джлюк': "JEDIKNIGHTLUKE",
	'жлюк': "JEDIKNIGHTLUKE",
	'jluke': "JEDIKNIGHTLUKE",
	'jediluke': "JEDIKNIGHTLUKE",
	'длюк': "JEDIKNIGHTLUKE",

	'лрей': "GLREY",
	'lrey': "GLREY",
	'глрей': "GLREY",
	'glrey': "GLREY",

	'wat': "WATTAMBOR",
	'ват': "WATTAMBOR",

	'кам': "KIADIMUNDI",
	'kam': "KIADIMUNDI",

	'лкайло': "SUPREMELEADERKYLOREN",
	'лекало': "SUPREMELEADERKYLOREN",
	'глкайл': "SUPREMELEADERKYLOREN",
	'lkylo': "SUPREMELEADERKYLOREN",
	'glkylo': "SUPREMELEADERKYLOREN"
}


help_msg = f'Список возможных команд:\n\n'
help_msg += '`!reg` или `!рег` — регистрация нового игрока у бота. Нужна для того, чтобы можно было запрашивать статистику по !stat имяВТелеге или команды на ТБ по !команды\nВарианты использования:\n'
help_msg += '`!reg кодСоюзника` = зарегистрировать себя с указанным кодом союзника\n'
help_msg += '`!reg имяВТелеге кодСоюзника` = зарегистрировать указанного пользователя телеграмма с указанным кодом союзника\n'
help_msg += 'Код союзника указывается в формате 123456789\n\n'
help_msg += '`!stat имяВТелеге` или `!стат имяВТелеге`\n'
help_msg += 'Вывод статистики GP и арены по зарегистрированному игроку с указанным именем в телеге.\n'
help_msg += 'Также возможен вариант `!stat кодСоюзника` для незарегистрированных игроков\n'
help_msg += 'Или просто `!stat` для запроса на себя (если ранее была регистрация)\n\n'
help_msg += '`!готовность персонаж`\n'
help_msg += 'Данные о том, у каких игроков гильдии есть указанный легендарный или эпический персонаж, и насколько готовы к нему остальные. Список поддерживаемых персонажей можно посмотреть, если ввести просто !готовность\n\n'

help_msg += '`!команды` или `!команды никВИгре`\n'
help_msg += 'Вывод текущих команд на взводы на себя или на указанного игрока.\n'
help_msg += 'Для данной команды нужно указать именно ник в игре. Можно попробовать ник в телеграме, но только если он зарегистрирован у бота\n'
help_msg += 'На себя (просто `!команды`) тоже сработает только если есть регистрация\n\n'

help_msg += 'Команды можно отправлять в личку боту, либо прямо в канале.\n\n'
help_msg += '`имяВТелеге` — *это username, который используется для обращения к пользователю* (не Имя-Фамилия, не ник).'
help_msg += 'Его нужно задать в настройках Телеграма. Боту можно передавать username с символом @ или без него'

extra_help_msg = f'Дополнительные команды для администраторов:\n\n'
extra_help_msg += '`!clearcommands`\nОчистить текущий список команд для взводов. Обычно не нужно, т.к. при получении данных от echobase команды перезатираются сами\n\n'
extra_help_msg += '`!tboverview`\nПросмотр краткой информации о заполняемости взводов на текущую фазу\n\n'
extra_help_msg += '`!listcommands`\nВывести полный список всех сохраненных команд (очень много текста)\n\n'
extra_help_msg += '`!sendallcommands`\nРазослать в личку зарегистрированным пользователям их персональные команды (глючит, пока лучше не пользоваться)\n\n'
extra_help_msg += '`!list` или `!список`\nСписок всех игроков, зарегистрированных у бота\n\n'
extra_help_msg += '`!forget имяВТелеге`\nОтменить регистрацию игрока с указанным username\n\n'
extra_help_msg += '`!up`\nОбновить состав и инвентарь всех игроков гильдии с сайта swgoh.gg (выполняется примерно 20 сек, нужно выполнить для корректной работы следующей команды, а также для команды !готовность)\n\n'
extra_help_msg += '`!checkregs`\nСравнение списка зарегистрированных у бота игроков и списка гильдии с сайта swgoh.gg\n\n'
extra_help_msg += '`!twinreg username code gamename`\nРегистрация твина с четко заданными параметрами\n\n'
extra_help_msg += '`!twinforget username`\nУдаление твина с указанным юзернеймом телеги (удаляется первый найденный, если несколько - надо повторить команду)\n\n'

msg_ready_help = f'Возможные варианты запросов:\n\n'
msg_ready_help += f'`!готовность траун`\n'
msg_ready_help += f'`!готовность c3po`\n'
msg_ready_help += f'`!готовность рей`\n'
msg_ready_help += f'`!готовность клюк`\n'
msg_ready_help += f'`!готовность чубака`\n'
msg_ready_help += f'`!готовность р2д2`\n'
msg_ready_help += f'`!готовность бб8`\n'
msg_ready_help += f'`!готовность палпатин`\n'
msg_ready_help += f'`!готовность реван`\n'
msg_ready_help += f'`!готовность древан`\n'
msg_ready_help += f'`!готовность падме`\n'
msg_ready_help += f'`!готовность сокол`\n'
msg_ready_help += f'`!готовность химера`\n'
msg_ready_help += f'`!готовность трея`\n'
msg_ready_help += f'`!готовность вампа`\n'
msg_ready_help += f'`!готовность хода`\n'
msg_ready_help += f'`!готовность джлюк`\n'
msg_ready_help += f'`!готовность лрей`\n'
msg_ready_help += f'`!готовность лкайло`'
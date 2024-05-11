#!usr/bin/env python
import re
import state
import telebot
import time
import traceback

BOT_NAME = "@MutuallyAssuredDestruction_bot"

# Format for timestamps used in exception messages printed on the server.
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Default values for game.
NUKES = 5				# Number of nukes each player starts with.
MONEY = 1000000000		# Amount of money each player starts with ($1 billion).
UPKEEP_PERIOD = 86400	# How often upkeep is charged, in seconds.
UPKEEP_COST = 50000000	# Upkeep cost of a single nuke ($50 million).
FLIGHT_TIME = 86400		# How long a nuke takes to reach its target, in seconds.
CITIES = 3				# Number of cities each player starts with.

# Dictionary of State objects keyed by chat ID (a number).
# Load state for all chats for which the bot has a file.
stateTable = state.State.loadAll()

with open("token", "r") as f:
	# Using unthreaded bot so I can catch and report exceptions the message
	# handlers may throw.
	bot = telebot.TeleBot(f.read(), parse_mode="MarkdownV2", threaded=False)

@bot.message_handler(commands = ["help"])
def help(message):
		output = telebot.formatting.escape_markdown("help - Send the help message.\n"
				+ "newgame - Create a new game.\n"
				+ "join - Join the game. Usage: \"/join my city's name; another city's name; a third city's name\n"
				+ "startgame - Start the game when all players are ready.\n"
				+ "scoreboard - See the current state of the game (players, remaining money, remaining nukes, remaining cities, etc.)\n"
				+ "nuke - Launch a nuke. Usage: \"/nuke City Name\".\n"
				+ "dismantle - Permanently dismantle a nuke and stop paying its upkeep cost.")
		bot.reply_to(message, output)

# Receive all messages and parse them as commands if valid.
@bot.message_handler(commands = ["newgame", "join", "startgame", "scoreboard", "nuke", "dismantle"])
def handle_command(message):
	chatId = str(message.chat.id)
	output = ""
	if chatId not in stateTable:
		# Create or load a state, depending on whether a file exists for this chat.
		stateTable[chatId] = state.State.create(chatId)
	s = stateTable[chatId]
	cmd = message.text
	cmd = re.sub(BOT_NAME, "", cmd)
	# Make commands case-insensitive, strip surrounding whitespace, and split
	# into command and arguments at spaces.
	cmd = cmd.lower().strip()
	cmd = cmd.lstrip("/")
	cmdSplit = cmd.split(" ", 1)

	#print("cmdSplit[0] = {0}".format(cmdSplit[0]))
	noGameOutput = telebot.formatting.escape_markdown("You must create a game to do that.")
	if cmdSplit[0] == "newgame":
		# TODO: This should require some kind of confirmation from a user to
		#	avoid accidentally resetting a game in progress.
		s.newGame(NUKES, MONEY, UPKEEP_PERIOD, UPKEEP_COST, FLIGHT_TIME)
		output = telebot.formatting.escape_markdown("New game created. Players may join now.")
	elif cmdSplit[0] == "join":
		if s.game:
			if len(cmdSplit) > 1:
				output = joinGame(s, cmdSplit[1], message.from_user)
			else:
				output = telebot.formatting.escape_markdown("You must list your city names when joining.")
		else:
			output = noGameOutput
	elif cmdSplit[0] == "startgame":
		if s.game:
			output = s.game.start()
		else:
			output = noGameOutput
	elif cmdSplit[0] == "scoreboard":
		if s.game:
			output = s.game.scoreboard()
		else:
			output = noGameOutput
	elif cmdSplit[0] == "nuke":
		if s.game:
			if len(cmdSplit) > 1:
				output = s.game.launch(message.from_user.id, cmdSplit[1])
			else:
				output = telebot.formatting.escape_markdown("This requires a target. Try \"/nuke City Name\"")
		else:
			output = noGameOutput
	elif cmdSplit[0] == "dismantle":
		if s.game:
			output = s.game.dismantle(message.from_user.id)
		else:
			output = noGameOutput

	if output != "":
		bot.reply_to(message, output)
	print("output = " + output)

	# Save after every command.
	s.save()

# s: A state object.
# citiesString: A semicolon delimited string containing city names.
# user: A telebot.types.User object representing the user sending the message.
def joinGame(s, citiesString, user):
	output = ""
	playerId = user.id
	playerName = user.username
	# Telebot's docs say username is optional but first name is required.
	# If username was None or empty, use the user's first name.
	if not playerName:
		playerName = user.first_name
	# Split the cities into a list and do input validation.
	cities = citiesString.split(";")

	# TODO: Figure out how long a city name can be before it interferes with
	# 		output formatting. Then, reject any name longer than that.
	for i in reversed(range(0, len(cities))):
		c = cities[i]
		# Replace all whitespace characters with single spaces.
		c = re.sub("\s+", " ", c)
		# Remove surrounding whitespace.
		c = c.strip()
		if not c:
			# If there wasn't anything valid in this city name, remove it from the list.
			del cities[i]
		else:
			# Otherwise, use the sanitized name.
			cities[i] = c
	if len(cities) < CITIES:
		output = "{0} cities are required.".format(CITIES)
	else:
		output = s.game.join(playerId, playerName, cities)
	return output


# Get any updates waiting on Telegram's servers.
updates = bot.get_updates()
while (True):
	time.sleep(2)
	try:
		# If we found updates, process them and acknowledge them when retrieving new updates.
		if len(updates) > 0:
			bot.process_new_updates(updates)
			updates = bot.get_updates(updates[-1].update_id + 1)
		# If we didn't find any updates, don't do any processing and don't acknowledge any updates.
		else:
			updates = bot.get_updates()
		# Iterate through all state objects and call Game.update() for any games
		# in progress.
		for chatId in stateTable:
			s = stateTable[chatId]
			if s.game and s.game.gameStarted and not s.game.gameOver:
				output = s.game.update()
				if output != "":
					# Split the output so it fits into Telegram messages.
					for string in telebot.util.smart_split(output):
						bot.send_message(chatId, string)
					# Something happened, so we'll save this state.
					s.save()
	except Exception as e:
		# There doesn't seem to be a way to find out which update caused an exception...
		# Throw out all of the updates we were trying to process. This will affect
		# all groups using the bot if any one of them causes an exception.
		if len(updates) > 0:
			updates = bot.get_updates(updates[-1].update_id + 1)
		print("Exception occurred at {0} UTC...".format(time.strftime(TIME_FORMAT, time.gmtime())))
		print(traceback.format_exc())

#!usr/bin/env python
import state
import re
import state
import sys
import telebot
import time

BOT_NAME = "@MutuallyAssuredDestruction_bot"

# Default values for game.
NUKES = 5				# Number of nukes each player starts with.
MONEY = 1000000000		# Amount of money each player starts with ($1 billion).
UPKEEP_PERIOD = 86400	# How often upkeep is charged, in seconds.
UPKEEP_COST = 50000000	# Upkeep cost of a single nuke ($50 million).
FLIGHT_TIME = 86400		# How long a nuke takes to reach its target, in seconds.

# Dictionary of State objects keyed by chat ID (a number).
stateTable = dict()

with open("token", "r") as f:
	bot = telebot.TeleBot(f.read(), parse_mode="MarkdownV2")

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
	chatId = message.chat.id
	output = ""
	if chatId not in stateTable:
		# Create or load a state, depending on whether a file exists for this chat.
		stateTable[chatId] = state.create(str(chatId))
	s = stateTable[chatId]
	cmd = message.text
	cmd = re.sub(BOT_NAME, "", cmd)
	# Make commands case-insensitive, strip surrounding whitespace, and split
	# into command and arguments at spaces.
	cmd = cmd.lower().strip()
	cmdSplit = cmd.split(" ", 1)

	if cmdSplit[0] == "newgame":
		# TODO: This should require some kind of confirmation from a user to
		#	avoid accidentally resetting a game in progress.
		s.newGame(NUKES, MONEY, UPKEEP_PERIOD, UPKEEP_COST, FLIGHT_TIME)
		output = "New game created. Players may join now."
	elif cmdSplit[0] == "join":
		# TODO: Write a join() function and do input validation on the city names.
		# For example, make sure the name has a maximum length and isn't something
		# trollish, like being all spaces or having more than one space between
		# words. Probably just use a regex to convert any instance of one or
		# more whitespace characters to a single space character.
	elif cmdSplit[0] == "startgame":
	elif cmdSplit[0] == "scoredboard":
	elif cmdSplit[0] == "nuke":
	elif cmdSplit[0] == "dismantle":
	
	if output != "":
		bot.reply_to(message, output)
	#print("output = " + output)

	# Save after every command.
	s.save()

# Load state for all chats for which the bot has a file.
# TODO: Load state

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
			if s.game.gameStarted and not s.game.gameOver:
				output = s.game.update()
				if output != "":
					for string in telebot.util.smart_split(output):
						bot.send_message(chatId, string)
	except:
		# Print exception info.
		print("\n{0}: {1}\n".format(sys.exc_info()[0], sys.exc_info()[1]))


#!usr/bin/env python
import telebot
import re

BOT_NAME = "@MutuallyAssuredDestruction_bot"

# Default values for game.
NUKES = 5				# Number of nukes each player starts with.
MONEY = 1000000000		# Amount of money each player starts with ($1 billion).
UPKEEP_PERIOD = 86400	# How often upkeep is charged, in seconds.
UPKEEP_COST = 50000000	# Upkeep cost of a single nuke ($50 million).

# Dictionary of State objects keyed by chat ID (a number).
stateTable = dict()

with open("token", "r") as f:
	bot = telebot.TeleBot(f.read(), parse_mode="MarkdownV2")

@bot.message_handler(commands = ["help"])
def help(message):
		output = telebot.formatting.escape_markdown("help - Send the help message.\n"
				+ "newgame - Create a new game.\n"
				+ "join - Join the game.\n"
				+ "startgame - Start the game when all players are ready.\n"
				+ "scoreboard - See the current state of the game (players, remaining money, remaining nukes, remaining cities, etc.)\n"
				+ "nuke - Launch a nuke. Use the form \"/nuke City Name\".\n"
				+ "dismantle - Permanently dismantle a nuke and stop paying its upkeep cost.")
		output += "\n\n" + telebot.formatting.mbold("testing...")
		output += "\n\n" + telebot.formatting.mbold("Active Players")
		output += "\nBob"
		output += "\n\t\tNew York"
		output += "\n\t\t" + telebot.formatting.mstrikethrough("Detroit")
		output += "\n\t\t" + telebot.formatting.mstrikethrough("Washington")
		output += "\n\n" + telebot.formatting.mbold("Eliminated Players")
		output += "\nAlice " + telebot.formatting.escape_markdown("(bankrupt)")
		output += "\n\t\tMoscow"
		output += "\n\t\t" + telebot.formatting.mstrikethrough("Stalingrad")
		output += "\n\t\t" + telebot.formatting.mstrikethrough("Kiev")
		output += "\nEve " + telebot.formatting.escape_markdown("(annihilated)")
		output += "\n\t\t" + telebot.formatting.mstrikethrough("Disneyland")
		output += "\n\t\t" + telebot.formatting.mstrikethrough("Santa's Workshop")
		output += "\n\t\t" + telebot.formatting.mstrikethrough("Narnia")
		bot.reply_to(message, output)

# Receive all messages and parse them as commands if valid.
# TODO: May want to make a separate function for each command. Not sure.
@bot.message_handler(commands = ["start", "newGame", "scoreboard", "launch", "dismantle"])
def handle_command(message):
	chatId = message.chat.id
	output = ""
	if chatId not in stateTable:
		# TODO: Create a new state object or load an existing state.
		# Will probably move this to a Start() function (see notes).
		pass # no-op
	else:
		# TODO: Set a local variable to the current chat's bot state.
		# Will probably move this to an InitializeBot() function (see notes).
		pass # no-op
	cmd = message.text
	cmd = re.sub(BOT_NAME, "", cmd)
	# Make commands case-insensitive and split into command and arguments at spaces.
	cmd = cmd.lower()
	cmdSplit = cmd.split(" ", 1)
	
	if output != "":
		bot.reply_to(message, output)
	#print("output = " + output)

	# Save after every command.
	s.save()

	
bot.infinity_polling()

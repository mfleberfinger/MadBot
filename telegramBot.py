#!usr/bin/env python
import telebot
import re

BOT_NAME = "@MutuallyAssuredDestruction_bot"

# Dictionary of State objects keyed by chat ID (a number).
gameTable = dict()

with open("token", "r") as f:
	bot = telebot.TeleBot(f.read(), parse_mode=None)

@bot.message_handler(commands = ["help"])
def help(message):
		output = ("start - Start the bot.\n" +
					"flee - Run away from a fight.")
		bot.reply_to(message, output)

# Receive all messages and parse them as commands if valid.
# TODO: May want to make a separate function for each command. Not sure.
@bot.message_handler(commands = ["start", "newGame", "scoreboard", "launch", "dismantle"])
def handle_command(message):
	chatId = message.chat.id
	output = ""
#	if chatId not in gameTable:
#		s = state.State(str(chatId))
#		g = game.Game(s)
#		gameTable[chatId] = g
#		if s.newGame:
#			output += ("Welcome, adventurer, to Generica, a land of infinite* possibilities!\n\n\n" +
#						"* Subject to technical and mechanical limitations. Other limitations may apply. " +
#						"Infinite does not necessarily mean interesting. Developer assumes no liability " +
#						"for any shortcomings, bugs, bad design, anti-features, or malfeasance. " +
#						"May cause cancer.\n\n\n")
#	else:
#		g = gameTable[chatId]
#		s = g.gameState
	cmd = message.text
	cmd = re.sub(BOT_NAME, "", cmd)
	# Make commands case-insensitive and split into command and arguments at spaces.
	cmd = cmd.lower()
	cmdSplit = cmd.split(" ", 1)
	
	if output != "":
		bot.reply_to(message, output)
	#print("output = " + output)

	# Save after every command.
	# telebot makes this the more convenient approach.
	#s.save()

	
bot.infinity_polling()

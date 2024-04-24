import datetime
import nuke
import player
import telebot

class Game:

	TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

	# startNukes: Number of nukes each player starts with.
	# startMoney: Amount of money each player starts with.
	# upkeepPeriod: How often (in seconds) upkeep cost is deducted.
	# upkeepCost: The cost per upkeep period of owning a nuke.
	# flightTime: How long a nuke takes to reach its target after launch, in seconds.
	def __init__(self, startNukes, startMoney, upkeepPeriod, upkeepCost, flightTime):
		self.startNukes = startNukes		# Number of nukes each player starts with.
		self.startMoney = startMoney		# Amount of money each player starts with.
		self.upkeepPeriod = upkeepPeriod	# How often upkeep is charged, in seconds.
		self.upkeepCost = upkeepCost		# The cost per upkeep period of owning a nuke.
		self.flightTime = flightTime		# How long a nuke takes to reach its target after launch, in seconds.
		self.activePlayers = dict()			# Players remaining in the game.
		self.eliminatedPlayers = dict()		# Players who have been eliminated.
		self.cityOwners = dict()			# Player IDs, keyed by city name.
		self.lastUpkeepTime = None			# The Last datetime at which the upkeep cost was applied. We will assume the server is using UTC.
		self.inFlight = list()				# List of nukes in flight, owners, targets, and launch times.
		self.gameOver = False				# True if the game has ended.
		self.gameStarted = False			# True if the game has started, meaning no new players may join.
		self.tzname = datetime.datetime.now().astimezone().tzname() # Time zone code (e.g. EDT, EST, UTC).

	# Add player to the game.
	# playerId: Unique identifier for the new player.
	# playerName: Player name displayed to users.
	# cityNames: List of names for this player's cities. Each city name must be
	#	unique within an instance of Game.
	def join(self, playerId, playerName, cityNames):
		output = "Error in Game.join()."
		claimedCityNames = list()
		for city in cityNames:
			if city in self.cityOwners:
				claimedCityNames.append(city)
		if self.gameStarted:
			output = "The game has started. No new players may join."
		elif playerId in self.activePlayers:
			output = "You've already joined, " + playerName + "."
		elif len(claimedCityNames) > 0:
			output = ("The following city names are already taken: " +
				", ".join(claimedCityNames))
		else:
			newPlayer = player.Player(playerId, playerName, cityNames, self.startNukes,
				self.startMoney)
			self.activePlayers[playerId] = newPlayer
			for city in cityNames:
				self.cityOwners[city] = playerId
			output = newPlayer.playerName + " has joined the game."
		return output
	
	# Close the game to new players and start playing.
	def start(self):
		output = "The game is already in progress."
		if len(self.activePlayers) < 2:
			output = "At least two players are required to start the game."
		elif not self.gameStarted:
			self.lastUpkeepTime = datetime.datetime.now()
			self.gameStarted = True
			output = "The game has started. Welcome to the Cold War."
		return output
	
	# Called when a player launches a nuke.
	# attackingPlayerId: Unique ID of the player launching the nuke.
	# targetCity: Name of the targeted city.
	def launch(self, attackingPlayerId, targetCity):
		output = "Error in Game.launch()."
		# Make sure the player exists and hasn't been eliminated.
		if attackingPlayerId not in self.activePlayers:
			output = "Only players who have not been eliminated may do that."
		# Make sure the target exists.
		elif targetCity not in self.cityOwners:
			output = "There is no city called " + targetCity + "."
		# Make sure the player has a nuke to launch.
		elif self.activePlayers[attackingPlayerId].nukes < 1:
			output = "You have nothing to launch."
		# Launch the nuke and generate appropriate output.
		else:
			attackingPlayerName = self.activePlayers[attackingPlayerId].playerName
			targetPlayerId = self.cityOwners[targetCity]
			targetPlayerName = ""
			if targetPlayerId in self.activePlayers:
				targetPlayerName = self.activePlayers[targetPlayerId].playerName
			else:
				targetPlayerName = self.eliminatedPlayers[targetPlayerId].playerName
			newNuke = nuke.Nuke(attackingPlayerId, targetCity, datetime.datetime.now())
			self.inFlight.append(newNuke)
			arrivalTime = newNuke.launchTime + datetime.timedelta(seconds=self.flightTime)
			output = ("LAUNCH WARNING: {0} has launched a missile at {1} (owned"
				" by {2}). The missile will reach {1} at {3} {4}.")
			# Perform any bookkeeping required by the Player object.
			self.activePlayers[attackingPlayerId].launch()
			output = output.format(attackingPlayerName, targetCity, targetPlayerName,
				arrivalTime.strftime(Game.TIME_FORMAT), self.tzname)
		return output

	# Dismantle a nuke.
	# The player for which to dismantle the nuke.
	def dismantle(self, playerId):
		output = "Error in Game.dismantle()."
		# Make sure the player exists and hasn't been eliminated.
		if playerId not in self.activePlayers:
			output = "Only players who have not been eliminated may do that."
		# Make sure the player has a nuke to dismantle.
		elif self.activePlayers[playerId].nukes < 1:
			output = "You have nothing to dismantle."
		else:
			self.activePlayers[playerId].dismantle()
			output = self.activePlayers[playerId].playerName + " has dismantled a weapon."
		return output
	
	# Returns a markdown formatted string describing the current state of the game.
	# The Telegram bot will need to split this into multiple messages in some
	#	cases.
	def getScoreboard(self):
		output = ""
		# Iterate through active players and display their information.
		for playerId in activePlayers
			p = activePlayers[playerId]
			output += telebot.formatting.munderline(telebot.formatting.mbold("Active Players"), False)
			output += "\n\n" + telebot.formatting.mbold(p.playerName)
			output += "\nMoney: "
			output += "\nNukes: "
			output += "\nCities:"
			output += "\n\t\tNew York"
		# Iterate through eliminated players and display their information.
		# Iterate through nukes in flight and display their information.
		return output

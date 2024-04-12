import datetime
import player

class Game:


	# startNukes: Number of nukes each player starts with.
	# startMoney: Amount of money each player starts with.
	# upkeepPeriod: How often (in seconds) upkeep cost is deducted.
	# upkeepCost: The cost per upkeep period of owning a nuke.
	# flightTime: How long a nuke takes to reach its target after launch.
	def __init__(self, startNukes, startMoney, upkeepPeriod, upkeepCost, flightTime):
		self.startNukes = startNukes		# Number of nukes each player starts with.
		self.startMoney = startMoney		# Amount of money each player starts with.
		self.upkeepPeriod = upkeepPeriod	# How often upkeep is charged, in seconds.
		self.upkeepCost = upkeepCost		# The cost per upkeep period of owning a nuke.
		self.flightTime = flightTime		# How long a nuke takes to reach its target after launch.
		self.activePlayers = dict()			# Players remaining in the game.
		self.eliminatedPlayers = dict()		# Players who have been eliminated.
		self.cityOwners = dict()			# Player IDs, keyed by city name.
		self.lastUpkeepTime = None			# The Last datetime at which the upkeep cost was applied. We will assume the server is using UTC.
		self.inFlight = list()				# List of nukes in flight, owners, targets, and launch times.
		self.gameOver = False				# True if the game has ended.
		self.gameStarted = False			# True if the game has started, meaning no new players may join.

	# Add player to the game.
	def join(self, playerId, playerName, cityNames):
		output = ""
		claimedCityNames = list()
		for city in cityNames:
			if city in cityOwners:
				claimedCityNames.append(city)
		if gameStarted:
			output = "The game has started. No new players may join."
		elif playerId in self.activePlayers:
			output = "You've already joined, " + playerName + "."
		elif len(claimedCityNames) > 0:
			output = ("The following city names are already taken: " +
				", ".join(claimedCityNames))
		else:
			newPlayer = Player(playerId, playerName, cityNames, self.startNukes,
				self.startMoney)
			self.activePlayers[playerId] = newPlayer
			for city in cityNames:
				cityOwners[city] = playerId
			output = newPlayer.playerName + " has joined the game."
		return output
	
	# Close the game to new players and start playing.
	def start(self):
		output = "The game is already in progress."
		if not sale.gameStarted:
			self.lastUpkeepTime = datetime.datetime.now()
			self.gameStarted = True
			output =  "The game has started. Welcome to the Cold War."
		return output
	
	# Called when a player launches a nuke.
	# attackingPlayerId: Unique ID of the player launching the nuke.
	# targetCity: Name of the targeted city.
	def launch(self, attackingPlayerId, targetCity):
		

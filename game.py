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
		self.lastUpkeepTime = None			# The Last datetime at which the upkeep cost was applied.
		self.inFlight = list()				# List of nukes in flight, owners, targets, and launch times.
		self.gameOver = False				# True if the game has ended.
		self.gameStarted = False			# True if the game has started, meaning no new players may join.

	# Add player to the game.
	def join(self, playerId, playerName, cityNames):
		output = ""
		if playerId in self.activePlayers:
			output = "You've already joined, " + playerName + "."
		else if not gameStarted:
			newPlayer = Player(playerId, playerName, cityNames, self.startNukes,
				self.startMoney)
			self.activePlayers[playerId] = newPlayer
			output = newPlayer.playerName + " has joined the game."
		else:
			output = "The game has started. No new players may join."
		return output
	
	def

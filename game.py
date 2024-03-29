import datetime

def __init__(self, upkeepPeriod, upkeepCost, flightTime):
	# How often upkeep is charged, in seconds.
	self.upkeepPeriod = upkeepPeriod
	self.upkeepCost = upkeepCost
	self.flightTime = flightTime
	# Active players, keyed by player ID.
	self.activePlayers = dict()
	# Eliminated players, keyed by player ID.
	self.eliminatedPlayers = dict()
	# The Last datetime at which the upkeep cost was applied.
	self.lastUpkeepTime = None
	# List of nukes in flight, owners, targets, and launch times.
	self.inFlight = list()
	self.gameOver = False
	self.gameStarted = False


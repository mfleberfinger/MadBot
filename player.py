class Player:

	# playerId: Unique identifier for this player.
	# playerName: What to call this player in any output.
	# cities: Collection of strings. Holds the names of the player's remaining
	#	cities.
	# nukes: Integer keeping track of the player's remaining nukes.
	# money: Integer keeping track of the player's remaining money.
	def __init__(self, playerId, playerName, cities, nukes, money):
		self.playerId = playerId
		self.playerName = playerName
		self.cities = cities
		self.nukes = nukes
		self.money = money
		# A string describing why the player was eliminated.
		# Likely values: "annihilated", "bankrupt"
		self.eliminationCause = None

	# Called when a player launches a nuke. Maybe this could include some
	# bookkeeping for endgame stats. For now, it just decrements the nukes
	# counter.
	def launch(self):
		self.nukes -= 1

	# Called when a player dismantles a nuke. Maybe this could include some
	# bookkeeping for endgame stats. For now, it just decrements the nukes
	# counter.
	def dismantle(self):
		self.nukes -= 1

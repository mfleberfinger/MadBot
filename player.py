def __init__(self, cities, nukes, money):
	self.cities = cities
	self.nukes = nukes
	self.money = money
	# A string describing why the player was eliminated.
	# Likely values: "annihilated", "bankrupt"
	self.eliminationCause = None

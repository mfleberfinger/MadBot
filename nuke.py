class Nuke:

	# owner: ID of the player who launched the nuke.                     
	# target: Name of the targeted city.                                 
	# launchTime: Datetime at which the nuke was launched.
	def __init__(self, owner, target, launchTime):
		self.owner = owner
		self.target = target
		self.launchTime = launchTime

import datetime
import locale
import nuke
import player
import telebot

# Used for easy currency formatting.
# The locale code ("en_US.UTF-8") might be system specific. It works on Ubuntu.
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

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
		self.upkeepPeriodDelta = datetime.timedelta(seconds=self.upkeepPeriod)	# Upkeep period in the format used by time math.
		self.upkeepCost = upkeepCost		# The cost per upkeep period of owning a nuke.
		self.flightTime = flightTime		# How long a nuke takes to reach its target after launch, in seconds.
		self.flightTimeDelta = datetime.timedelta(seconds=flightTime)	# Flight time in the format used by time math.
		self.activePlayers = dict()			# Players remaining in the game.
		self.eliminatedPlayers = dict()		# Players who have been eliminated.
		self.cityOwners = dict()			# Player IDs, keyed by city name.
		self.lastUpkeepTime = None			# The Last datetime at which the upkeep cost was applied. We will assume the server is using UTC.
		self.inFlight = list()				# List of nukes in flight, owners, targets, and launch times.
		self.gameOver = False				# True if the game has ended.
		self.gameStarted = False			# True if the game has started, meaning no new players may join.
		self.tzname = datetime.datetime.now().astimezone().tzname()	# Time zone code (e.g. EDT, EST, UTC).

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
		return telebot.formatting.escape_markdown(output)
	
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
			output = "Only active players may do that."
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
			arrivalTime = newNuke.launchTime + self.flightTimeDelta
			output = ("LAUNCH WARNING: {0} has launched a missile at {1} (owned"
				" by {2}). The missile will reach {1} at {3} {4}.")
			# Perform any bookkeeping required by the Player object.
			self.activePlayers[attackingPlayerId].launch()
			output = output.format(attackingPlayerName, targetCity, targetPlayerName,
				arrivalTime.strftime(Game.TIME_FORMAT), self.tzname)
		return telebot.formatting.escape_markdown(output)

	# Dismantle a nuke.
	# The player for which to dismantle the nuke.
	def dismantle(self, playerId):
		output = "Error in Game.dismantle()."
		# Make sure the player exists and hasn't been eliminated.
		if playerId not in self.activePlayers:
			output = "Only active players may do that."
		# Make sure the player has a nuke to dismantle.
		elif self.activePlayers[playerId].nukes < 1:
			output = "You have nothing to dismantle."
		else:
			self.activePlayers[playerId].dismantle()
			output = self.activePlayers[playerId].playerName + " has dismantled a missile."
		return output
	
	# Returns a markdown formatted string describing the current state of the game.
	# The Telegram bot will need to split this into multiple messages in some
	#	cases.
	def getScoreboard(self):
		output = ""
		# Iterate through active players and display their information.
		output += telebot.formatting.munderline(telebot.formatting.mbold("Active Players"), False)
		if len(self.activePlayers) == 0:
			output += "\n\nNone"
		for playerId in self.activePlayers:
			p = self.activePlayers[playerId]
			output += "\n\n" + telebot.formatting.mbold(p.playerName)
			output += "\nMoney: " + telebot.formatting.escape_markdown(locale.currency(p.money, grouping=True))
			output += "\nMissiles: " + str(p.nukes)
			output += "\nCities:"
			for city in p.cities:
				output += "\n\t\t" + telebot.formatting.escape_markdown(city)
			for city in p.destroyedCities:
				output += "\n\t\t" + telebot.formatting.mstrikethrough(city)
		# Iterate through eliminated players and display their information.
		output += "\n\n\n" + telebot.formatting.munderline(telebot.formatting.mbold("Eliminated Players"), False)
		if len(self.eliminatedPlayers) == 0:
			output += "\n\nNone"
		for playerId in self.eliminatedPlayers:
			p = self.eliminatedPlayers[playerId]
			output += "\n\n" + telebot.formatting.mbold(p.playerName + " (" + p.eliminationCause + ")")
			output += "\nMoney: " + telebot.formatting.escape_markdown(locale.currency(p.money, grouping=True))
			output += "\nMissiles: " + str(p.nukes)
			output += "\nCities:"
			for city in p.cities:
				output += "\n\t\t" + telebot.formatting.escape_markdown(city)
			for city in p.destroyedCities:
				output += "\n\t\t" + telebot.formatting.mstrikethrough(city)
		# Iterate through nukes in flight and display their information.
		output += "\n\n\n" + telebot.formatting.munderline(telebot.formatting.mbold("Missiles In-Flight"), False)
		if len(self.inFlight) == 0:
			output += "\n\nNone"
		nukeString = "Target: {0}\nArrival: {1} {2}\nOwner: {3}"
		for nuke in self.inFlight:
			if nuke.owner in self.activePlayers:
				owner = self.activePlayers[nuke.owner]
			else:
				owner = self.activePlayers[nuke.owner]
			arrivalTime = nuke.launchTime + self.flightTimeDelta
			output += "\n\n" + telebot.formatting.escape_markdown(nukeString.format(nuke.target, 
				arrivalTime.strftime(Game.TIME_FORMAT), self.tzname, owner.playerName))
		return output
	
	# Should be called periodically to update the state of the game.
	# Deducts money for upkeep, decides when missiles reach their targets and
	# handles the result, eliminates players as needed, decides whether the
	# game has ended, etc.
	def update(self):
		if not self.gameStarted:
			raise RuntimeError("Game.Update() was called without starting the game.")
		elif self.gameOver:
			raise RuntimeError("Game.Update() was called after the game ended.")
		output = ""
		output += self.__updateNukes()
		output += self.__updateUpkeep()
		output += self.__updateEliminations()
		output += self.__updateEndgame()
		# Remove trailing whitespace (including newlines).
		output = output.rstrip()
		return telebot.formatting.escape_markdown(output)
	
	# Check whether missiles have reached their targets, handle any bookkeeping
	# associated with destruction of cities, and return related output.
	def __updateNukes(self):
		output = ""
		# Iterate through in-flight missiles, decide whether they've arrived at
		# their targets, and handle the effects if they have.
		toRemove = list()
		i = 0
		for missile in self.inFlight:
			if (missile.launchTime + self.flightTimeDelta) <= datetime.datetime.now():
				toRemove.append(i)
				# Find the target city's owner.
				cityOwnerId = self.cityOwners[missile.target]
				if cityOwnerId in self.activePlayers:
					cityOwner = self.activePlayers[cityOwnerId]
				else:
					cityOwner = self.eliminatedPlayers[cityOwnerId]
				# Find the missile's owner.
				if missile.owner in self.activePlayers:
					missileOwner = self.activePlayers[missile.owner]
				else:
					missileOwner = self.eliminatedPlayers[missile.owner]
				# If the city hasn't already been destroyed, move it to the
				# owners destroyedCities list. If it has, include that in the
				# output.
				if missile.target in cityOwner.cities:
					cityOwner.cities.remove(missile.target)
					cityOwner.destroyedCities.append(missile.target)
					output += "CITY DESTROYED: {0}'s missile destroyed {1}.\n"
				else:
					output += ("{0}'s missile made the crater formerly known "
						" as {1} slightly deeper.\n")
				output = output.format(missileOwner.playerName, missile.target)
			i += 1
		for j in reversed(toRemove):
			del self.inFlight[j]
		return output

	# Deduct upkeep costs and return related output.
	def __updateUpkeep(self):
		output = ""
		if datetime.datetime.now() >= self.lastUpkeepTime + self.upkeepPeriodDelta:
			self.lastUpkeepTime = datetime.datetime.now()
			for playerId in self.activePlayers:
				p = self.activePlayers[playerId]
				totalUpkeep = p.nukes * self.upkeepCost
				p.money -= totalUpkeep
				output += ("{0} pays {1} in upkeep costs for {2} missiles and is "
					"left with {3}.\n")
				output = output.format(p.playerName, locale.currency(totalUpkeep, grouping=True),
					p.nukes, locale.currency(p.money, grouping=True))
		return output

	# Check for annihilation and bankruptcy, do related bookkeeping, and return
	# related output.
	def __updateEliminations(self):
		output = ""
		# Copy the dictionary's keys into a new list so we can iterate through
		#	the dictionary while deleting from it.
		keys = list(self.activePlayers.keys())
		for playerId in keys:
			p = self.activePlayers[playerId]
			if len(p.cities) <= 0:
				p.eliminationCause = "annihilated"
				self.eliminatedPlayers[playerId] = self.activePlayers.pop(playerId)
				output += p.playerName + " has been annihilated.\n"
			elif p.money <= 0:
				p.eliminationCause = "bankrupt"
				self.eliminatedPlayers[playerId] = self.activePlayers.pop(playerId)
				output += p.playerName + "'s economy has collapsed.\n"
		return output

	# Check for the endgame conditions, end the game if appropriate, and return
	# related output.
	def __updateEndgame(self):
		output = ""
		noNukes = False
		# Determine whether there are any nukes left in the game.
		if len(self.inFlight) == 0:
			noNukes = True
			keys = list(self.activePlayers.keys())
			i = 0
			while noNukes and i < len(keys):
				if self.activePlayers[keys[i]].nukes > 0:
					noNukes = False
				i += 1
		# The game ends when only one player is left and there are no nukes in
		# flight, or when there are no nukes remaining in flight or in stockpiles.
		if (len(self.activePlayers) <= 1 and len(self.inFlight) == 0) or noNukes:
			self.gameOver = True
			output += "\nGAME OVER\n\n"
			# If no players remain, the game ends in a draw.
			if len(self.activePlayers) == 0:
				output += "ALL PLAYERS ELIMINATED... The only winning move is not to play."
			# If only one player is left standing, that player wins.
			elif len(self.activePlayers) == 1:
				output += "VICTORY: {0} wins!"
				output = output.format(next(iter(self.activePlayers.values())).playerName)
			else:
				possibleWinners = list(self.activePlayers.values())
				# If two or more players remain, the player with the most cities
				# wins.
				maxCities = 0
				for p in possibleWinners:
					if len(p.cities) > maxCities:
						maxCities = len(p.cities)
				toRemove = list()
				for p in possibleWinners:
					if len(p.cities) < maxCities:
						toRemove.append(p.playerId)
				i = 0
				while i < len(possibleWinners):
					if possibleWinners[i].playerId in toRemove:
						del possibleWinners[i]
					else:
						i += 1
				# If two or more remaining players hold the same number of
				# cities, the player with the most money remaining out of the
				# players with the most cities wins.
				if len(possibleWinners) > 1:
					maxMoney = 0
					for p in possibleWinners:
						if p.money > maxMoney:
							maxMoney = p.money
					toRemove = list()
					for p in possibleWinners:
						if p.money < maxMoney:
							toRemove.append(p.playerId)
					i = 0
					while i < len(possibleWinners):
						if possibleWinners[i].playerId in toRemove:
							del possibleWinners[i]
						else:
							i += 1
				# If two or more remaining players have the same number of cities
				# and the same amount of money, the game ends in a draw.
				if len(possibleWinners) > 1:
					output += "Draw between the following players:\n"
					for p in possibleWinners:
						output  += p.playerName + "\n"
					output.rstrip("\n")
				else:
					output += "VICTORY: {0} wins!"
					output = output.format(possibleWinners[0].playerName)
		return output

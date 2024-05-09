import game
import os
import pickle
import re

class State:

	SAVE_DIRECTORY = "savedGames/"
	# This extension is being added to state files to make sure loadAll() doesn't
	# attempt to load other files that might somehow get added to the save directory.
	FILE_EXTENSION = ".state"
	# File extension with any regex metacharacters escaped.
	regexExtension = re.escape(FILE_EXTENSION)

	# Load a State from a file, if it exists, or create a new State.
	def create(saveName):
		if os.path.isfile(State.SAVE_DIRECTORY + saveName + State.FILE_EXTENSION):
			state = load(saveName)
		else:
			state = State(saveName)
		return state

	def load(saveName):
		with open(State.SAVE_DIRECTORY + saveName + State.FILE_EXTENSION, "rb") as f:
			return pickle.load(f)

	# Load all existing state files and return the state objects in a dictionary
	# keyed by save name (the filename without the extension).
	def loadAll():
		filenames = os.listdir(State.SAVE_DIRECTORY)
		stateTable = dict()
		for name in filenames:
			if name.endswith(State.FILE_EXTENSION):
				saveName = re.sub(regexExtension, "", name)
				stateTable[saveName] = load(saveName)
		return stateTable
					

	def save(state):
		with open(State.SAVE_DIRECTORY + self.saveName + State.FILE_EXTENSION, "w+b") as f:
			return pickle.dump(self, f)
	
	def __init__(self, saveName):
		self.saveName = saveName
		self.game = None
	
	def newGame(self, startNukes, startMoney, upkeepPeriod, upkeepCost, flightTime):
		self.game = Game(startNukes, startMoney, upkeepPeriod, upkeepCost, flightTime)
	
	def endGame(self)
		self.game = None

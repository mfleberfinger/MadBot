import game
import os
import pickle

class State:

	SAVE_DIRECTORY = "savedGames/"

	# Load a State from a file, if it exists, or create a new State.
	def create(saveName):
		if os.path.isfile(State.SAVE_DIRECTORY + saveName):
			state = load(saveName)
		else:
			state = State(saveName)
		return state

	def load(saveName):
		with open(State.SAVE_DIRECTORY + saveName, "rb") as f:
			return pickle.load(f)

	def save(state):
		with open(State.SAVE_DIRECTORY + self.saveName, "w+b") as f:
			return pickle.dump(self, f)
	
	def __init__(self, saveName):
		self.saveName = saveName
		self.game = None
	
	def newGame(self, startNukes, startMoney, upkeepPeriod, upkeepCost, flightTime):
		self.game = Game(startNukes, startMoney, upkeepPeriod, upkeepCost, flightTime)
	
	def endGame(self)
		self.game = None

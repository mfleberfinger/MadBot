import game

def startGame():
	g = game.Game(5, 375000000, 0, 15000000, 0)
	g.join("1", "Bob", ["New York", "Denver", "Washington"])
	g.join("2", "Alice", ["The Shire", "Gondor", "Mordor"])
	g.join("3", "Eve", ["Moscow", "Pripyat", "Stalingrad"])
	g.start()
	return g

def bobWinsWar(g):
	print(g.launch("1", "The Shire"))
	print(g.launch("1", "Gondor"))
	print(g.launch("1", "Mordor"))
	print(g.launch("1", "Moscow"))
	print(g.launch("1", "Pripyat"))
	print(g.launch("2", "Stalingrad"))

def extinction(g):
	print(g.launch("1", "The Shire"))
	print(g.launch("1", "Gondor"))
	print(g.launch("1", "Mordor"))
	print(g.launch("1", "Moscow"))
	print(g.launch("1", "Pripyat"))
	print(g.launch("2", "Stalingrad"))
	print(g.launch("3", "New York"))
	print(g.launch("3", "Denver"))
	print(g.launch("3", "Washington"))

def dismantleAll(g):
	for i in range(0,5):
		print(g.dismantle("1"))
		print(g.dismantle("2"))
		print(g.dismantle("3"))

def twoWayDrawWar(g):
	print(g.launch("1", "Moscow"))
	dismantleAll(g)

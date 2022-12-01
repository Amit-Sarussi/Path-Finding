width = 500
height = 500
squerePixel = 20
squereWidth = width//squerePixel
# 0 for walkable (white), 1 for Wall (black), 2 for A, 3 for B 
gameData = [0 for squeres in range((width//squerePixel)*(height//squerePixel))]

def printBoard(gameData: list):
	for vertical in range(squereWidth):
		print('\n', end='')
		for horizontal in range(squereWidth):
			print(f'[{gameData[horizontal+vertical*squereWidth]}]', end='')

def changeValue(gameData: list,value: int, pos: tuple, squeresWidth: int):
	x = pos[0] -1
	y = pos[1] -1

	gameData[x + y*len(gameData)//squeresWidth] = value
	return gameData

gameData = changeValue(gameData,1, (2,2), width//squerePixel)
gameData = changeValue(gameData,2, (3,2), width//squerePixel)
printBoard(gameData)

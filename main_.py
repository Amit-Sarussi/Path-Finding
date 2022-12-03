width = 500
height = 500
pixelPerSquere = 20
squeresPerLine = width//pixelPerSquere

EndSim = False
Data = {}
for x in range(squeresPerLine):
	for y in range(squeresPerLine):
		Data[x+y*squeresPerLine] = dict(value = 0, dir = 0, sum = -1)

def changeValue(Data: dict,Value: int, Pos: tuple, Dir: tuple = (0,0), Sum = -1):
	Data[(Pos[0])+(Pos[1])*squeresPerLine] = {'value': Value, 'dir': Dir, 'sum' : Sum}

changeValue(Data, 3, (4,3))
changeValue(Data, 2, (7,7))

LastPointSolved = [0,0]
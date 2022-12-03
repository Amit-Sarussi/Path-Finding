import pygame, main_, math, time
from main_ import *

''' CONSTANTS VALUES '''
BLACK = (0, 0, 0)
WHITE = (255,255,255)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500
''' SCENE '''

def main():
    FirstStep = 0
    Step = 0
    # Setup
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)

    while True:

    # Change grid colors by gameData
        colorGrid()

    # Draw the grid lines on top of the colored grid
        drawGrid()
        
        EndSim = main_.EndSim
        if EndSim == False:
        # Find the Points A and B
            Data = main_.Data
            PointA = [0,0,0]
            PointB = [0,0,0]
            squereWidth = main_.squeresPerLine
            for i in Data:
                if Data[i]["value"] == 2:
                    PointA = [i%squereWidth,i//squereWidth]
                if Data[i]["value"] == 3:
                    PointB = [i%squereWidth,i//squereWidth]
        # Assign Points Values
            PointA = tuple(PointA)
            PointB = tuple(PointB)

        # Draw Outline on a point
            
            if FirstStep > 0:
                importentData = {}
                
                #for i in len(importentData):
                for i in range(len(Data)):
                    if Data[i]["sum"] != -1 and Data[i]["value"] == 4:
                        importentData[i] = Data[i]
                smallestSum = min((int(d['sum'])) for d in importentData.values())
                smallestIndex = 0 
                for i in importentData:
                    if importentData[i]['sum'] == smallestSum:
                        smallestIndex = i
                        break
                
                solve(I2P(smallestIndex), squereWidth, PointA, PointB, main_.LastPointSolved)
                main_.LastPointSolved = [I2P(smallestIndex)[0],I2P(smallestIndex)[1]]
                FirstStep += 1
            elif FirstStep == 0:
                main_.LastPointSolved = [PointA[0],PointA[1]]
                solve(PointA, squereWidth, PointA, PointB, main_.LastPointSolved)
                FirstStep = 1

        if Step == 2:
            print('f')
            makePath((main_.LastPointSolved[0],main_.LastPointSolved[1]))   
            Step += 1

    # Quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    Step = 1
                if event.key == pygame.K_1:
                    Step = 2
                    print('g')
                if event.key == pygame.K_2:
                    print(main_.Data[105])
        pygame.display.update()

def I2P(x: int):
    return (x%squeresPerLine, x//squeresPerLine)

def drawGrid():
    blockSize = main_.pixelPerSquere #Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x,y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

def colorGrid():
    Data = main_.Data
    Data = [i['value'] for i in Data.values()]
    squerePixel = main_.pixelPerSquere
    squereWidth = main_.squeresPerLine
    for data in range(len(Data)):
        rect = pygame.Rect((data//squereWidth)*squerePixel, (data%squereWidth)*squerePixel, squerePixel, squerePixel)
        if Data[data] == 0: # Normal
            pygame.draw.rect(SCREEN, (255,255,255), rect)
        if Data[data] == 1: # Blocked
            pygame.draw.rect(SCREEN, (0,0,0), rect)
        if Data[data] == 2: # A 
            pygame.draw.rect(SCREEN, (0,0,255), rect)
        if Data[data] == 3: # B
            pygame.draw.rect(SCREEN, (3, 132, 252), rect)
        if Data[data] == 4: # Outline
            pygame.draw.rect(SCREEN, (86, 252, 3), rect)
        if Data[data] == 5: # Invested Point
            pygame.draw.rect(SCREEN, (255,0,0), rect)
        if Data[data] == 6: # Path
            pygame.draw.rect(SCREEN, (215, 3, 252), rect)


def solve(Point: tuple, squereWidth, PointA, PointB, lastPoint):
    direction = (lastPoint[0]-Point[0],lastPoint[1]-Point[1])
    print(direction, lastPoint, Point)
    for y in range(3):
        for x in range(3):
            a,b = x,y
            a += Point[0]-1
            b += Point[1]-1
            if (a,b) != (Point[0], Point[1]): # If the point is not the center
                if (Data[a+b*squereWidth]['value']==3): # If the current point is B
                    main_.EndSim = True
                elif (Data[a+b*squereWidth]['value']==0): # normal
                    if ((b == Point[1]) or (b == Point[1] + 1) or (b == Point[1] - 1)) and ((a == Point[0]) or (a == Point[0] + 1) or (a == Point[0] - 1)):
                        changeValue(Data, 4, (a,b), (direction), calculatePoints(PointA, PointB, (a,b)))
            elif (Data[Point[0]+Point[1]*squereWidth]['value'] == 0 or Data[Point[0]+Point[1]*squereWidth]['value'] == 4):
                print(Data[a+b*squeresPerLine]['dir'], 'gdfdfg')
                changeValue(Data, 5, (a,b), Data[a+b*squeresPerLine]['dir'])
                print(a,b,direction,"hello")
                print(Data[a+b*squeresPerLine])
                main_.LastPointSolved = [a,b]
                print('placed red')     

def calculatePoints(PointA: tuple, PointB: tuple, Point: tuple):
    #calculate Point A:
    Awidth = max(PointA[0],Point[0]) - min(PointA[0],Point[0])
    Aheight = max(PointA[1],Point[1]) - min(PointA[1],Point[1])
    Adistance = ((math.sqrt(Awidth**2+Aheight**2))*10)//1
    
    #Calculate Point B:
    Bwidth = max(PointB[0],Point[0]) - min(PointB[0],Point[0])
    Bheight = max(PointB[1],Point[1]) - min(PointB[1],Point[1])
    Bdistance = ((math.sqrt(Bwidth**2+Bheight**2))*10)//1

    return int(Bdistance) + int(Adistance)

def makePath(Point: tuple):
    finishPath = False
    point = list([Point[0],Point[1]])
    for i in range(100):#finishPath != True:
        #print(point)
        index = point[0]+1 + point[1]*squeresPerLine
        changeValue(Data, 6, (point[0],point[1]), (Data[index]['dir']))
        #check if we finished path
        if(Data[index-1-squeresPerLine]['value'] == 2 or
        Data[index-squeresPerLine]['value'] == 2 or
        Data[index+1-squeresPerLine]['value'] == 2 or
        Data[index-1-2*squeresPerLine]['value'] == 2 or
        Data[index+1-2*squeresPerLine]['value'] == 2 or
        Data[index-1-3*squeresPerLine]['value'] == 2 or
        Data[index-3*squeresPerLine]['value'] == 2 or
        Data[index+1-3*squeresPerLine]['value'] == 2):
            finishPath = True
            print('finished Path')
            break

        else:
            point[0] += Data[index]['dir'][0]
            point[1] += Data[index]['dir'][1]
main()
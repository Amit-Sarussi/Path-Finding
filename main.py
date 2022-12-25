import math
import pygame
import pgrid


#  --- BUILD THE BOARD ---
colors = [(255,255,255), (0,0,0), (0,0,255),(255,0,0),(0,255,0), (51, 204, 255), (255, 51, 153)]
board = pgrid.board(600,8, colors)


#  --- MODIFY LEVEL STRUCTURE ---
PointA = (1,1)
PointB = (6,6)

board.find(PointA[0],PointA[1]).modify(Value=2) #Point A
board.find(PointB[0],PointB[1]).modify(Value=5) #Point B
board.find(4,4).modify(Value=1)

# --- COLORS THE PATH AFTER IT WAS MADE ---
def finishPath(x,y):
    isFinished = False
    while isFinished != True:
        board.find(x,y).modify(Value=6)
        #Check for isFinished:
        if lookAround(x,y,2):
            isFinished = True
        else:
            x,y = board.find(x,y).Direction[0], board.find(x,y).Direction[1]
    else:
        if board.find(x,y).Value == 3:
            board.find(x,y).Value = 6

# --- CHECK AT THE 8 SPOTS AROUNT SINGLE POINT AND SCOUT FOR CERTEIN VALUE ---
def lookAround(x,y,Value = 5):
    isFounded = False
    for y_ in range(-1,2): 
        for x_ in range(-1,2):
            if x + x_ > 0 and x + x_ < board.cellsPerLine and y + y_ > 0 and y + y_ < board.cellsPerLine:
                if board.find(x+x_,y+y_).Value == Value and any([x_,y_]) != 0:
                    isFounded = True
                    board.find(x,y).modify(Value=3)
    return isFounded

# --- CHECK HOW MUCH DISTANCE OF SQUARES TO MOVE IN ORDER TO REACH THE POINT ---
def calcDistance(xPos,yPos,AxPos,AyPos):
    sum = 0
    xDiff = AxPos-xPos #2
    yDiff = AyPos-yPos #1
    while not (yDiff == 0 and xDiff == 0):
        if xDiff > 0 and yDiff > 0: #Diagonal RD
            sum += 14
            xDiff -= 1
            yDiff -= 1
            xPos += 1
            yPos += 1
        if xDiff < 0 and yDiff > 0: #Diagonal LD
            sum += 14
            xDiff += 1
            yDiff -= 1
            xPos -= 1
            yPos += 1
        if xDiff > 0 and yDiff < 0: #Diagonal RU
            sum += 14
            xDiff -= 1
            yDiff += 1
            xPos -= 1
            yPos -= 1
        if xDiff < 0 and yDiff < 0: #Diagonal LU
            sum += 14
            xDiff += 1
            yDiff += 1
            xPos -= 1
            yPos -= 1
        elif xDiff > 0 and yDiff == 0: # Move Right
            sum += 10
            xDiff -= 1
            xPos += 1
        elif xDiff < 0 and yDiff == 0: # Move Left
            sum += 10
            xDiff += 1
            xPos -= 1
        elif yDiff > 0 and xDiff == 0: # Move Down
            sum += 10
            yDiff -= 1
            yPos -= 1
        elif yDiff < 0 and xDiff == 0: # Move Up
            sum += 10
            yDiff += 1
            yPos -= 1
    return sum

    

# --- INVESTIGATE ALL THE 8 POINTS AROUND A SINGLE POINT (MAKING IT RED) ---
def findAround(xPos,yPos, xA, yA, xB, yB):
    if  board.find(xPos, yPos).Value == 0 or board.find(xPos, yPos).Value == 4:
        board.find(xPos, yPos).modify(Value=3)
    for y in range(-1,2): 
        for x in range(-1,2):
            if any([x,y]) != 0:
                #Calculate Distance From point to Point A
                Adist = calcDistance(xPos+x, yPos+y, xA, yA)
                
                #Calculate Distance From point to Point B
                Bdist = calcDistance(xPos+x, yPos+y, xB, yB)

                #Modify Data
                if (board.find(xPos + x, yPos + y).Value == 0 or board.find(xPos + x, yPos + y).Value == 4):
                    board.find(xPos + x, yPos + y).modify(Value=4, Distance=Adist+Bdist)
                if board.find(xPos + x, yPos + y).Direction == None:
                    board.find(xPos + x, yPos + y).modify(Direction=(xPos,yPos))
                    #print((xPos + x, yPos + y),Adist, Bdist, board.find(xPos + x, yPos + y).Distance, board.find(xPos + x, yPos + y).Direction)


# --- INITIALIZING THE GAME LOOP ---
CurrentPoint = PointA
gameEnded = False
pygame.init()

screen = pygame.display.set_mode([600, 600])

running = True
step = 0

while running:

    # --- EVENT HANDLER ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    board.drawBoard(screen)
    if step < 100:
        if gameEnded != True:
            findAround(CurrentPoint[0],CurrentPoint[1],PointA[0],PointA[1],PointB[0],PointB[1])
            # Look for the smallest distance Green point and assign it to the current point
            smallestDist = math.inf
            smHcost = math.inf
            for x in range(board.cellsPerLine):
                for y in range(board.cellsPerLine):
                    if board.find(x,y).Value == 4:
                        if board.find(x,y).Distance < smallestDist:
                            smallestDist = board.find(x,y).Distance
                            CurrentPoint = [x,y]     
            for x in range(board.cellsPerLine):
                for y in range(board.cellsPerLine):
                    if board.find(x,y).Value == 4:
                        if board.find(x,y).Distance == smallestDist:
                            if calcDistance(x, y, PointB[0], PointB[1]) <= smHcost:
                                smHcost = calcDistance(x, y, PointB[0], PointB[1])
                                CurrentPoint = [x,y]   

        gameEnded = lookAround(CurrentPoint[0],CurrentPoint[1])
        if gameEnded:
            finishPath(CurrentPoint[0],CurrentPoint[1])
        step+=1
        
    pygame.display.flip()

pygame.quit()
#1DRobot.py
from scratches.ForLoopLab.graphics import *
import random
facing = "L"
#2 is a coin to collect, 0s are the square, 1 is the robot.
grid = [0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
coinsCollected = 0


def spawnCoin():
    #randomly select an index from a list and change it to a coin / change it to a 2
    #1) make sure that we dont remove a robot
    #2) make sure that the coin spawns at least 2 squares from the robot
    global grid
    ranIndex = random.randint(0, len(grid)-1)
    robotIndex = getRobotIndex()
    while not (ranIndex < robotIndex - 2 or ranIndex > robotIndex + 2):
        ranIndex = random.randint(0, len(grid)-1)
    grid[ranIndex] = 2

def turnAround():
    global facing
    #changes the direction that the robot is facing
    if facing == "L":
        facing = "R"
    elif facing == "R":
        facing = "L"
def moveForward():
    #move the robot forward one square in the
    #direction that it is facing
    i = getRobotIndex()
    #based on the direction it is facing, change
    #the square next to it to '1' and its current
    #square to '0'
    global facing, grid, coinsCollected
    if facing == "R" and i+1 < len(grid):
        if grid[i+1] == 2: #is the square we're moving to a coin?
            coinsCollected += 1
            spawnCoin()
            updateCoinsCollectedText()
        grid[i+1] = 1
        grid[i] = 0
    elif facing == "L" and i-1 >= 0:
        if grid[i-1] == 2: #is the square we're moving to a coin?
            coinsCollected += 1
            spawnCoin()
            updateCoinsCollectedText()
        grid[i-1] = 1
        grid[i] = 0
    else:
        print("Robot cannot move.")

#returns the current index of the robot
def getRobotIndex():
    global grid
    for i in range(len(grid)):
        if grid[i] == 1:
            return i
    print("Robot cannot be found")
    return -1

def printGrid():
    global grid
    output = "["
    for i in range(len(grid)):
        if grid[i] == 0:
            output += " "
        elif grid[i] == 1 and facing == "R":
            output += ">"
        elif grid[i] == 1 and facing == "L":
            output += "<"
        elif grid[i] == 2:
            output += 'o'
    output += "]"
    print(output)

def drawGrid(win):
    global grid
    sqSize = 20
    yOffset = 20
    xOffset = 600 - (sqSize*len(grid))
    xOffset /= 2
    # undraw all rect and triangles before redrawing them (prevents lag)
    for item in win.items:
        if type(item) != Text:
            item.undraw()
    for i in range(len(grid)):

        rect = Rectangle(Point(i*sqSize, yOffset), Point((i+1)*sqSize, sqSize + yOffset))
        rect.move(xOffset, 0)
        rect.setFill("black")
        rect.draw(win)
        if grid[i] == 1: #robot space - triangle <| or |>
            if facing == "L":
                robot = Polygon(Point((i+1)*sqSize, yOffset),
                                Point((i+1)*sqSize, yOffset + sqSize),
                                Point(i*sqSize, yOffset + sqSize/2))
            elif facing == "R":
                robot = Polygon(Point(i*sqSize, yOffset),
                                Point(i*sqSize, yOffset + sqSize),
                                Point((i+1)*sqSize, yOffset + sqSize/2))
            robot.move(xOffset, 0)
            robot.setFill("blue")
            robot.draw(win)

        elif grid[i] == 2: #circle for the coin
           coin = Circle(Point((i+0.5)*sqSize, yOffset*1.5), sqSize/2)
           coin.move(xOffset, 0)
           coin.setFill("yellow")
           coin.setOutline("black")
           coin.draw(win)

def drawCoinsCollectedText(win):
    global coinsText
    p1 = Point(300, 100)
    coinsString = "Coins collected: " + str(coinsCollected)
    coinsText = Text(p1, coinsString)
    coinsText.setFill("black")
    coinsText.draw(win)

def updateCoinsCollectedText():
    global coinsText
    coinsText.setText("Coins collected: " + str(coinsCollected))



def drawDirections(win):

    p1 = Point(300, 300)
    directionString = "Collect all the yellow coins.\n" \
                      " Press 'w' to move forward\n" \
                      "     'a' or 'd' to turn\n" \
                      "        'q' to quit"
    text = Text(p1, directionString)
    text.setFill("black")
    text.draw(win)


def graphicsMain():
    global grid, facing
    win = GraphWin("1D Robot", 600, 600, autoflush=False)
    gameOver = False
    drawCoinsCollectedText(win)
    drawDirections(win)

    while not gameOver:
        print("\n" * 15)

        update(30)
        drawGrid(win)
        userInput = win.checkKey()
        print(userInput)
        #input("Press 'w' to move forward, 'a' or 'd' to turn or 'q' tp quit")
        if userInput == 'w':
            moveForward()
            drawGrid(win)
        elif userInput == 'a' or userInput == 'd':
            turnAround()
            drawGrid(win)
        elif userInput == 'q':
            gameOver = True

if __name__ == '__main__':
    #consoleMain()
    graphicsMain()
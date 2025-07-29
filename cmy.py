from cmu_graphics import *
import random

def onAppStart(app):
    app.startScreen = True
    app.count = 0
    app.rows = 17
    app.cols = 17
    app.cellSize = 20
    app.width = app.cols*app.cellSize
    app.height = app.cellSize*app.rows
    app.setMaxShapeCount(5000)
    app.level = 1
    app.playerRadius = app.cellSize*0.4
    app.gameOver = False
    app.maze = [[1 for _ in range(app.cols)] for _ in range(app.rows)]
    app.angle = 270
    app.game3D = False
    startRow, startCol = 1, 1
    app.maze[startRow][startCol] = 0
    carveMaze(app, startRow, startCol)

    


    app.maze[0][1] = 0
    for col in range(app.cols - 2, 0, -1):
        if app.maze[app.rows - 2][col] == 0:
            app.maze[app.rows - 1][col] = 0
            app.exitCol = col
            break
    app.start = (0, 1)
    app.end = (app.rows - 1, app.exitCol)

    app.playerX = startCol * app.cellSize + app.cellSize / 2
    app.playerY = startRow * app.cellSize + app.cellSize / 2
    app.speed = 3
    app.cubes = []
    generateCubes(app)

def onKeyHold(app, keys):
    dx, dy = 0, 0
    if 'a' in keys:
        dx -= 5
    if 'd' in keys:
        dx += 5
    if 'w' in keys:
        dy -= 5
    if 's' in keys:
        dy += 5

    newX = app.playerX + dx
    newY = app.playerY + dy

    
    if isLegal(app, newX, newY):
        app.playerX = newX
        app.playerY = newY

    col = int(app.playerX // app.cellSize)
    row = int(app.playerY // app.cellSize)
    app.cubes = [(r, c) for (r, c) in app.cubes
                 if not (r == row and c == col)]
    if row == app.rows - 1 and col == app.exitCol and len(app.cubes) == 0:
        print("Maze completed! Generating a new one...")
        app.level += 1
        resetMaze(app)
def resetMaze(app):
    
    app.maze = [[1 for _ in range(app.cols)] for _ in range(app.rows)]
    startRow, startCol = 1, 1
    app.maze[startRow][startCol] = 0
    carveMaze(app, startRow, startCol)
    app.maze[0][1] = 0
    for col in range(app.cols - 2, 0, -1):
        if app.maze[app.rows - 2][col] == 0:
            app.maze[app.rows - 1][col] = 0
            app.exitCol = col
            break
    app.playerX = startCol * app.cellSize + app.cellSize / 2
    app.playerY = startRow * app.cellSize + app.cellSize / 2
    generateCubes(app)
    

def onMousePress(app, mouseX, mouseY):
    if app.startScreen:
        # Check if click is inside the Start button
        btnX, btnY, btnW, btnH = app.width/2 - 75, app.height * 0.7, 150, 50
        if btnX <= mouseX <= btnX + btnW and btnY <= mouseY <= btnY + btnH:
            app.startScreen = False

def generateCubes(app):
    while len(app.cubes) < app.level:
        row = random.randint(1, app.rows - 2)
        col = random.randint(1, app.cols - 2)
        if app.maze[row][col] == 0 and (row, col) not in [app.start, app.end]:
            app.cubes.append((row, col))

def getDistance(app, x, y):
    return ((x - app.playerX) ** 2 + (y - app.playerY) ** 2) ** 0.5

def getHitType(app, row, col):
    if app.maze[row][col] == 1:
        return 'wall'
    elif (row, col) == app.start:
        return 'start'
    elif (row, col) == app.end:
        return 'end'
    elif (row, col) in app.cubes:
        return 'cube'
    return None
def carveMaze(app, startRow, startCol):
    stack = [(startRow, startCol)]  # fixed variable name

    while stack:
        row, col = stack[-1]  # peek the top of the stack

        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions)

        carved = False
        for dr, dc in directions:
            newRow, newCol = row + dr, col + dc
            if (0 < newRow < app.rows - 1) and (0 < newCol < app.cols - 1):
                if app.maze[newRow][newCol] == 1:
                    wallRow = row + dr // 2
                    wallCol = col + dc // 2
                    app.maze[wallRow][wallCol] = 0
                    app.maze[newRow][newCol] = 0
                    stack.append((newRow, newCol))
                    carved = True
                    break  # only carve one direction at a time

        if not carved:
            stack.pop()  # backtrack
def isLegal(app, x, y):
    r = app.playerRadius
    if not (r <= x <= app.width - r and r <= y <= app.height - r):
        return False
    points = [
        (x - r, y), (x + r, y),
        (x, y - r), (x, y + r)
    ]
    for px, py in points:
        row = int(py // app.cellSize)
        col = int(px // app.cellSize)
        if app.maze[row][col] == 1:
            return False
        if (row, col) == (app.end) and len(app.cubes)>0:
            return False

    return True

def redrawAll(app):
    if app.startScreen:
        drawRect(0, 0, app.width, app.height, fill='black')
        drawLabel('MAZE ESCAPE', app.width/2, 80, size=40, fill='white', bold=True)
        drawLabel('Use W/A/S/D to move and turn.', app.width/2, 140, size=20, fill='lightGray')
        drawLabel('Press F to toggle 3D view.', app.width/2, 160, size=20, fill='lightGray')
        drawLabel('Green is the start. Red is the end', app.width/2, 180, size=20, fill='lightGray')
        drawLabel('Collect all the blue cubes before exiting', app.width/2, 200, size=20, fill='lightGray')
        
        # Draw the Start button
        btnX, btnY, btnW, btnH = app.width/2 - 75, app.height * 0.7, 150, 50
        drawRect(btnX, btnY, btnW, btnH, fill='green', border='white', borderWidth=3)
        drawLabel('Start Game', app.width/2, btnY + btnH/2, size=24, fill='white', bold=True)
        return  # Don't draw the game yet if start screen is active
    for row in range(app.rows):
            for col in range(app.cols):
                color = 'black' if app.maze[row][col] == 1 else 'white'
                drawRect(col * app.cellSize, row * app.cellSize,
                         app.cellSize, app.cellSize, fill=color)

    drawRect(1 * app.cellSize, 0, app.cellSize, app.cellSize, fill='green')
    drawRect(app.exitCol * app.cellSize, (app.rows - 1) * app.cellSize,
                 app.cellSize, app.cellSize, fill='red')


    drawCircle(app.playerX, app.playerY, app.playerRadius, fill='blue', rotateAngle=app.angle)
    for (row, col) in app.cubes:
        drawRect(col * app.cellSize+5, row * app.cellSize+5,
                app.cellSize-10, app.cellSize-10, fill="blue")
    

  
    


    # Draw entrance (green) and exit (red)
    drawRect(1 * app.cellSize, 0, app.cellSize, app.cellSize, fill='green')
    drawRect(app.exitCol * app.cellSize, (app.rows - 1) * app.cellSize,
             app.cellSize, app.cellSize, fill='red')

    # Draw player circle (blue)
    drawCircle(app.playerX, app.playerY, app.playerRadius, fill='blue')

runApp()

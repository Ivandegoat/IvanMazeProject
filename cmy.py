from cmu_graphics import *
import random
import math

def onAppStart(app):
    app.wallBreaksLeft = 3
    app.lastKeyPressed = 'd'
    app.timer = 30
    app.gameOver = False
    app.levelScreen = False
    app.startScreen = True
    app.count = 0
    app.rows = 17
    app.cols = 17
    app.cellSize = 25
    app.width = app.cols*app.cellSize
    app.height = app.cellSize*app.rows
    app.level = 1
    app.playerRadius = app.cellSize*0.4
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
    app.cubes = []
    generateCubes(app)
    app.steps = 0
    
def onStep(app):
    if app.startScreen:
        return
    app.steps += 1
    if app.gameOver:
        return
    if app.steps%30 == 0:
        
        app.timer -= 1
        if app.timer == 0:
            app.gameOver = True

    if app.levelScreen:
        app.levelScreenTimer -= 1
        if app.levelScreenTimer <= 0:
            app.levelScreen = False
        return

        

def onMousePress(app, mouseX, mouseY):
    if app.startScreen:
        # Check if click is inside the Start button
        btnX, btnY, btnW, btnH = app.width/2 - 75, app.height * 0.7, 150, 50
        if btnX <= mouseX <= btnX + btnW and btnY <= mouseY <= btnY + btnH:
            app.startScreen = False
def onKeyPress(app, key):

    if key == 'f':
        if app.count % 2 == 1:
            app.playerRadius = app.cellSize * 0.4
        else:
            app.playerRadius = app.cellSize * 0.1
        app.game3D = not app.game3D
        app.count += 1

    # Snap player to center of the cell to avoid wall collision
        col = int(app.playerX // app.cellSize)
        row = int(app.playerY // app.cellSize)
        if app.maze[row][col] == 0:
            app.playerX = col * app.cellSize + app.cellSize / 2
            app.playerY = row * app.cellSize + app.cellSize / 2
    elif key == 'e' and app.wallBreaksLeft > 0:
        angle = math.radians(app.angle if app.game3D else
        {'w': 270, 'a': 180, 's': 90, 'd': 0}.get(app.lastKeyPressed, 0))
        for r in range(1, 100):
            rayX = app.playerX + r * app.cellSize/10 * math.cos(angle)
            rayY = app.playerY + r * app.cellSize/10 * math.sin(angle)
            row = int(rayY // app.cellSize)
            col = int(rayX // app.cellSize)
            if 0 < row < app.rows-1 and 0 < col < app.cols-1:
                if app.maze[row][col] == 1:
                    app.maze[row][col] = 0
                    app.wallBreaksLeft -= 1
                    break
    if key in ['w', 'a', 's', 'd']:
        app.lastKeyPressed = key
#Learned mae generating algorithm last year in my math class.
#Didn't look up any codes
def carveMaze(app,startRow, startCol):
    stack = [(startRow, startCol)]
    while stack:
        row, col = stack[-1]
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
                    break
        if not carved:
            stack.pop()

def onKeyHold(app, keys):
    if app.gameOver:
        if 'r' in keys:
            app.level = 1
            app.gameOver = False
            resetMaze(app)
        return

    dx, dy = 0, 0
    # Always allow turning independently of movement
    if app.game3D:
        # Turn first
        if 'a' in keys:
            app.angle -= 11
        if 'd' in keys:
            app.angle += 11
        app.angle %= 360

        # Then move forward/backward relative to angle
        if 'w' in keys:
            dx += 4 * math.cos(math.radians(app.angle))
            dy += 4 * math.sin(math.radians(app.angle))
        if 's' in keys:
            
            dx -= 4 * math.cos(math.radians(app.angle))
            dy -= 4 * math.sin(math.radians(app.angle))

    else:
        # 2D mode: simple dx, dy based on keys
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
    app.levelScreen = True
    app.levelScreenTimer = 20
    app.timer = 30
    app.wallBreaksLeft = 3

def generateCubes(app):
    while len(app.cubes) < app.level:
        row = random.randint(1, app.rows - 2)
        col = random.randint(1, app.cols - 2)
        if app.maze[row][col] == 0 and (row, col) not in [app.start, app.end]:
            app.cubes.append((row, col))

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
        if (row, col) == (app.start):
            return False
        if (row, col) == (app.end) and len(app.cubes)>0:
            return False

    return True

def redrawAll(app):
    if app.gameOver:
        drawRect(0,0,app.width,app.height, fill = 'black')
        drawLabel("Game Over", app.width//2, app.height//2-10,
                  fill = "red", size=45, font = "Times New Roman")
        drawLabel("Press r to restart",app.width//2, app.height//2+30,
                   fill = "white", size=14)
        return
    if app.levelScreen:
        drawRect(0, 0, app.width, app.height, fill='black')
        drawLabel(f'Level {app.level}', app.width/2, app.height/2,
                   size=50, fill='white')
        return
    if app.startScreen:
        for row in range(app.rows):
            for col in range(app.cols):
                color = 'black' if app.maze[row][col] == 1 else 'white'
                drawRect(col * app.cellSize, row * app.cellSize,
                         app.cellSize, app.cellSize, fill=color)
        drawRect(0,0, app.width,app.height, fill = "blue")
        drawLabel('MAZE ESCAPE', app.width/2, app.height-400, size=50, 
                  fill='white', bold=True)
        drawLabel('Use W/A/S/D to move and turn.', app.width/2, app.height-360 ,
                   size=20, fill='lightGray')
        drawLabel('Press F to toggle 3D view.', app.width/2,
                   app.height-340, size=20, fill='lightGray')
        drawLabel('You can only play fullscreen in 3D mode',
                   app.width/2, app.height-320, size=20, fill='lightGray')
        drawLabel('Timer goes faster in 2d mode', app.width/2,
                   app.height-300, size=20, fill='lightGray')
        drawLabel('Collect all the pink cubes before exiting',
                   app.width/2, app.height-280, size=20, fill='lightGray')
        
        drawLabel('Wall Break (E):', app.width//2, app.height-250,
                   size=16, fill ="white")
        drawLabel('- Press E to break the wall you\'re facing', app.width//2,
                   app.height-230, size=16, fill="white")
        drawLabel('- 3 uses per game', app.width//2, app.height-210, size=16,
                   fill="white")
        drawLabel('- In 2D: breaks the last direction you walked', app.width//2,
                   app.height-190, size=16, fill="white")
        drawLabel('- In 3D: breaks the wall you\'re looking at', app.width//2,
                   app.height-170, size=16, fill = "white")
        drawLabel('- Cannot break border walls', app.width//2, app.height-150,
                   size=16, fill = "white")

        # Draw the Start button
        btnX, btnY, btnW, btnH = app.width/2 - 75, app.height * 0.7, 150, 50
        drawRect(btnX, btnY, btnW, btnH, fill='green', border='white',
                  borderWidth=3)
        drawLabel('Start Game', app.width/2, btnY + btnH/2, size=24,
                   fill='white', bold=True)
        return  # Don't draw the game yet if start screen is active
    if app.game3D:
        draw3DView(app)
        
    else:
        
        for row in range(app.rows):
            for col in range(app.cols):
                color = 'black' if app.maze[row][col] == 1 else 'white'
                drawRect(col * app.cellSize, row * app.cellSize,
                         app.cellSize, app.cellSize, fill=color)

        drawRect(1 * app.cellSize, 0, app.cellSize, app.cellSize, fill='green')
        drawRect(app.exitCol * app.cellSize, (app.rows - 1) * app.cellSize,
                 app.cellSize, app.cellSize, fill='red')


        drawCircle(app.playerX, app.playerY, app.playerRadius, fill='blue',
                    rotateAngle=app.angle)
        for (row, col) in app.cubes:
            drawRect(col * app.cellSize+5, row * app.cellSize+5,
                app.cellSize-10, app.cellSize-10, fill="coral")
        minutes = app.timer // 60
        seconds = app.timer % 60
        timeText = f"{minutes:02}:{seconds:02}"
        drawLabel(f"Time Left: {timeText}", app.width//2, 10, size=18,
                   bold=True, fill='white')
        drawLabel(f"Breaks left: {app.wallBreaksLeft}", app.width//2,
                   app.height-10, size=18, bold=True, fill='white')

# HELPER: draw the 3D raycasting view
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

#Watched a lot of videos about raycasting
#https://youtu.be/ECqUrT7IdqQ?feature=shared
#https://lodev.org/cgtutor/raycasting.html
def draw3DView(app):
    stepRad = math.radians(0.45) # 200
    rayCount = 200
    sliceWidth = app.width / rayCount
    startRad = math.radians(app.angle) - (stepRad * (rayCount - 1) / 2)
    rayLength = 100

    rayHits = []

    # Cast rays
    for i in range(rayCount):
        #Bigger angle for each ray
        angle = startRad + i * stepRad
        for r in range(1, rayLength + 1):
            #go from 1 to 100 radius length and see if it hits everything
            rayX = app.playerX + r * math.cos(angle)
            rayY = app.playerY + r * math.sin(angle)
            row = int(rayY // app.cellSize)
            col = int(rayX // app.cellSize)

            if not (0 <= row < app.rows and 0 <= col < app.cols):
                break

            hitType = getHitType(app, row, col)
            if hitType:
                dist = getDistance(app, rayX, rayY)
                rayHits.append((i, dist, hitType))
                break

    drawRect(0,0, app.width, app.height, fill='olive')
    drawRect(0,0, app.width, app.height//2,fill='goldenrod')

    # Dark gradient overlay
    drawRect(0, 0, app.width, app.height, fill=gradient('white', 'black'),
              opacity=80)
    
    
    # Render vertical slices
    for i, dist, kind in rayHits:
        x = i * sliceWidth
        height = app.height / dist * 10
        y = app.height / 2 - height / 2
        op = max(5, min(100, 20000 / (dist ** 1.5)))

        colors = {'wall': 'olive', 'start': 'green', 'end': 'red',
                   'cube': 'lightpink'}
        drawRect(x, y, sliceWidth, height, fill=colors[kind], opacity=op)
    
    drawLabel(f"Cubes left: {len(app.cubes)}", app.width//2, 50,bold=True,
               size = 18)
    minutes = app.timer // 60
    seconds = app.timer % 60
    timeText = f"{minutes:02}:{seconds:02}"
    drawLabel(f"Time Left: {timeText}", app.width//2, 80, size=18, bold=True,
               fill='black')
    drawLabel(f"Breaks left: {app.wallBreaksLeft}", app.width//2, 110, size=18,
               bold=True, fill='black')
runApp()
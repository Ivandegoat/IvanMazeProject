from cmu_graphics import *
import random

def onAppStart(app):
    app.rows = 21
    app.cols = 31
    app.cellSize = 20
    app.width = app.cols * app.cellSize
    app.height = app.rows * app.cellSize
    app.maze = [[1 for _ in range(app.cols)] for _ in range(app.rows)]

    startRow, startCol = 1, 1
    app.maze[startRow][startCol] = 0
    carveMaze(app, startRow, startCol)

    app.maze[0][1] = 0  # entrance
    for col in range(app.cols - 2, 0, -1):
        if app.maze[app.rows - 2][col] == 0:
            app.maze[app.rows - 1][col] = 0  # exit
            app.exitCol = col
            break

    # Player position in pixels (center of start cell)
    app.playerX = startCol * app.cellSize + app.cellSize / 2
    app.playerY = startRow * app.cellSize + app.cellSize / 2
    app.playerRadius = app.cellSize * 0.4

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
    for row in range(app.rows):
        for col in range(app.cols):
            color = 'black' if app.maze[row][col] == 1 else 'white'
            drawRect(col * app.cellSize, row * app.cellSize,
                     app.cellSize, app.cellSize,
                     fill=color)

    # Draw entrance (green) and exit (red)
    drawRect(1 * app.cellSize, 0, app.cellSize, app.cellSize, fill='green')
    drawRect(app.exitCol * app.cellSize, (app.rows - 1) * app.cellSize,
             app.cellSize, app.cellSize, fill='red')

    # Draw player circle (blue)
    drawCircle(app.playerX, app.playerY, app.playerRadius, fill='blue')

runApp()

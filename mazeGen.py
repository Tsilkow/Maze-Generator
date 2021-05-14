import glob
import random
import sys
from PIL import Image,ImageDraw
from math import pi, sin, cos

dimensions = (51, 51)
tileSize = 16
tileVerticies = 6
start = (25, 25)
wallColor = (0, 0, 160)
corridorColor = (0, 0, 0)

if len(sys.argv) > 1: dimensions[0] = int(sys.argv[1])
if len(sys.argv) > 2: dimensions[1] = int(sys.argv[2])
if len(sys.argv) > 3: tileSize = float(sys.argv[3])
if len(sys.argv) > 4: tileVerticies = int(sys.argv[4])
if len(sys.argv) > 5: start[0] = int(sys.argv[5])
if len(sys.argv) > 6: start[1] = int(sys.argv[6])

if tileVerticies == 4:
    width  = dimensions[0] * tileSize
    height = dimensions[1] * tileSize
elif tileVerticies == 6:
    width = dimensions[0] * tileSize
    height = (dimensions[1] * 0.75 + 0.25) * tileSize

width = int(width)
height = int(height)
    
print(width, height)

im = Image.new('RGBA', (width, height), "#000000ff")
draw = ImageDraw.Draw(im)

def drawTile(x, y, color):
    
    if tileVerticies == 4:
        draw.polygon([( x      * tileSize,  y      * tileSize),
                      ((x + 1) * tileSize,  y      * tileSize),
                      ((x + 1) * tileSize, (y + 1) * tileSize),
                      ( x      * tileSize, (y + 1) * tileSize)],
                     fill = color)
    elif tileVerticies == 6:
        draw.polygon([((x + 0.5 + 0.5 * (y % 2)) * tileSize, (y * 0.75       ) * tileSize),
                      ((x + 1   + 0.5 * (y % 2)) * tileSize, (y * 0.75 + 0.25) * tileSize),
                      ((x + 1   + 0.5 * (y % 2)) * tileSize, (y * 0.75 + 0.75) * tileSize),
                      ((x + 0.5 + 0.5 * (y % 2)) * tileSize, (y * 0.75 + 1   ) * tileSize),
                      ((x       + 0.5 * (y % 2)) * tileSize, (y * 0.75 + 0.75) * tileSize),
                      ((x       + 0.5 * (y % 2)) * tileSize, (y * 0.75 + 0.25) * tileSize)],
                     fill = color)

def getNeighbour(x, y, d):
    if tileVerticies == 4:
        if   d == 0: return ( 0, -1)
        elif d == 1: return ( 1,  0)
        elif d == 2: return ( 0,  1)
        elif d == 3: return (-1,  0)
    elif tileVerticies == 6 and y % 2 == 0:
        if   d == 0: return ( 0, -1)
        elif d == 1: return ( 1,  0)
        elif d == 2: return ( 0,  1)
        elif d == 3: return (-1,  1)
        elif d == 4: return (-1,  0)
        elif d == 5: return (-1, -1)
    elif tileVerticies == 6 and y % 2 == 1:
        if   d == 0: return ( 1, -1)
        elif d == 1: return ( 1,  0)
        elif d == 2: return ( 1,  1)
        elif d == 3: return ( 0,  1)
        elif d == 4: return (-1,  0)
        elif d == 5: return ( 0, -1)

data = [[0 for i in range(dimensions[0])] for j in range(dimensions[1])]
toExamine = [start]
visited = [[0 for i in range(dimensions[0])] for j in range(dimensions[1])]

visited[start[0]][start[1]] = 1
data[start[0]][start[1]] = 1
drawTile(start[0], start[1], wallColor)
maxStep = 0
frames = [[]]

while len(toExamine) > 0:
    examined = toExamine[-1]
    deadEnd = 1
    step = data[examined[0]][examined[1]]
    maxStep = max(step+1, maxStep)
    while len(frames) <= maxStep: frames.append([])

    dirs = [i for i in range(tileVerticies)]
    random.shuffle(dirs)

    for d in dirs:
        #
        connector = (examined[0] + getNeighbour(examined[0], examined[1], d)[0],
                     examined[1] + getNeighbour(examined[0], examined[1], d)[1])
        neighbour = (connector[0] + getNeighbour(connector[0], connector[1], d)[0],
                     connector[1] + getNeighbour(connector[0], connector[1], d)[1])
        #print(neighbour)

        if (neighbour[0] >= 0 and neighbour[0] < dimensions[0] and
            neighbour[1] >= 0 and neighbour[1] < dimensions[1]) and visited[neighbour[0]][neighbour[1]] == 0:
            #print(d)
            data[connector[0]][connector[1]] = step+1
            data[neighbour[0]][neighbour[1]] = step+1
            frames[step+1].append(connector)
            frames[step+1].append(neighbour)
            visited[neighbour[0]][neighbour[1]] = 1
            toExamine.append(neighbour)
            deadEnd = 0
            break
        
    if deadEnd == 1: toExamine.remove(examined)

for s in range(maxStep):
    for c in frames[s]:
        drawTile(c[0], c[1], wallColor)
        
    im.save("output4/" + "{:07d}".format(s) + " maze", "PNG")
    print("output4/" + "{:07d}".format(s) + " maze")
                
# making a gif out of it
img, *imgs = [Image.open(f) for f in sorted(glob.glob("output4/* maze"))]
img.save(fp="out4.gif", format='GIF', append_images=imgs, save_all=True, duration=1, loop=0)

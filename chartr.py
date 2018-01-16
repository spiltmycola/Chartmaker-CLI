import argparse
import json
import math

class Point2D:
    def __init__(self, xCoord, yCoord):
        self.X = xCoord
        self.Y = yCoord

    def __str__(self):
        return "self.X: %0.2f\nself.Y: %0.2f\n" % (self.X, self.Y)

def vectorAdd2D(pointA, pointB):
    return Point2D(pointA.X + pointB.X, pointA.Y + pointB.Y)

''' Read Default Styles '''
defaultsFile = open('defaultstyles.json')
defaultStyles = json.loads(defaultsFile.read())

''' Argument parser'''
parser = argparse.ArgumentParser(description='Transpile')
parser.add_argument('inFileName', type=str, help="name of file to be transpiled")
parser.add_argument('--out', type=str, default="out.html", help="name of output file (Default: out.html)")
args = parser.parse_args()

try:
    dataFile = open(args.inFileName,"r")
except IOError as detail:
    print(detail)
    exit()
dataObject = json.loads(dataFile.read())
outFile = open(args.out,"w")

center = Point2D(0,0)
radius = 0
itemValues = []

'''--- Transpiler Checks and Reading in Data -----------------------------------------------------------'''

''' Key Existence Checks '''
if 'center' not in dataObject.keys():
    print("\'center\' has not been defined.")
    exit()
if 'radius' not in dataObject.keys():
    print("\'radius\' has not been defined.")
    exit()
if 'items' not in dataObject.keys():
    print("\'items\' have not been defined.")
    exit()

''' Value Validity Checks '''
if not dataObject['center']:
    print("\'center\' is empty.")
    exit()
try:
    centerArray = dataObject['center'].split(',')
    center.X = float(centerArray[0])
    center.Y = float(centerArray[1])
except:
    print("\'center\' must be of format: \"float,float\".")
    exit()

if not dataObject['radius']:
    print("\'radius\' is empty.")
    exit()
try:
    radius = float(dataObject['radius'])
except:
    print("\'radius\' must be a float.")

if not dataObject['items']:
    print("\'items\' is empty.")
    exit()
try:
    for item in dataObject['items']:
        itemValues.append(float(item['value']))
except:
    print("All items should have a \'value\' key with a float value.")

'''--- Actual Calculations --------------------------------------------------------------------------'''

itemValueTotal = 0
for i in range(len(itemValues)):
    itemValueTotal += itemValues[i]

''' Convert item values to radians '''
for i in range(len(itemValues)):
    itemValues[i] /= itemValueTotal
    itemValues[i] *= 2*math.pi

''' Finding list of key points on circumference '''
points = []
curAngle = 0
for i in range(len(itemValues)):
    relativePos = Point2D(math.sin(curAngle)*100, -math.cos(curAngle)*100)
    points.append(vectorAdd2D(relativePos, center))
    curAngle += itemValues[i]

''' Output to svg format '''
outFile.write("""<svg height=\"%d\" width=\"%d\">
    """ %(center.Y+radius+10, center.X+radius+10))
for i in range(len(itemValues)):
    #Centre Point 
    outFile.write("<path d=\"M%d,%d " %(center.X, center.Y))
    
    #Radius
    outFile.write("L%d,%d " %(points[i].X, points[i].Y))
    
    #Arc
    if i == len(itemValues) - 1:
        outFile.write("A%d,%d 0 0,1 %d,%d " %(radius, radius, points[0].X, points[0].Y))
    else:
        outFile.write("A%d,%d 0 0,1 %d,%d " %(radius, radius, points[i+1].X, points[i+1].Y))
    
    #End + Options
    #Take default styles if not specified
    if 'stroke' not in dataObject.keys():
        stroke = defaultStyles['stroke']
    else:
        stroke = dataObject['stroke']
    if 'stroke-linejoin' not in dataObject.keys():
        strokeLinejoin = defaultStyles['stroke-linejoin']
    else:
        strokeLinejoin = dataObject['stroke-linejoin']
    if 'stroke-opacity' not in dataObject.keys():
        strokeOpacity = defaultStyles['stroke-opacity']
    else:
        strokeOpacity = dataObject['stroke-opacity']
    if 'stroke-width' not in dataObject.keys():
        strokeWidth = defaultStyles['stroke-width']
    else:
        strokeWidth = dataObject['stroke-width']
    if 'color' not in dataObject['items'][i].keys():
        fill = defaultStyles['fill']
    else:
        fill = dataObject['items'][i]['color']

    outFile.write("""Z\" 
        stroke=\"%s\"
        stroke-linejoin=\"%s\"
        stroke-opacity=%d
        stroke-width=%d
        fill=\"%s\"
    />"""%(stroke, strokeLinejoin, strokeOpacity, strokeWidth, fill))
outFile.write("\n</svg>")
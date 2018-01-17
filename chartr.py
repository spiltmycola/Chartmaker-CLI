import argparse
import json
import math
from simplegeom import *

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

centre = Point2D(0,0)
radius = 0
itemValues = []

'''--- Transpiler Checks and Reading in Data -----------------------------------------------------------'''

''' Key Existence Checks '''
if 'centre' not in dataObject.keys():
    print("\'centre\' has not been defined.")
    exit()
if 'radius' not in dataObject.keys():
    print("\'radius\' has not been defined.")
    exit()
if 'items' not in dataObject.keys():
    print("\'items\' have not been defined.")
    exit()

''' Value Validity Checks '''
if not dataObject['centre']:
    print("\'centre\' is empty.")
    exit()
try:
    centreArray = dataObject['centre'].split(',')
    centre.X = float(centreArray[0])
    centre.Y = float(centreArray[1])
except:
    print("\'centre\' must be of format: \"float,float\".")
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

percentages = []

''' Convert item values to radians '''
for i in range(len(itemValues)):
    itemValues[i] /= itemValueTotal
    percentages.append(itemValues[i]*100)
    itemValues[i] *= 2*math.pi

''' Finding list of key points on circumference '''
points = []
curAngle = 0
arcCentres = []
for i in range(len(itemValues)):
    relativePos = Point2D(math.sin(curAngle)*radius, -math.cos(curAngle)*radius)
    points.append(vectorAdd2D(relativePos, centre))
    curAngleBefore = curAngle
    curAngle += itemValues[i]
    arcCentreAngle = (curAngleBefore + curAngle)/2
    relativeArcCentre = Point2D(math.sin(arcCentreAngle)*radius, -math.cos(arcCentreAngle)*radius)
    arcCentres.append(vectorAdd2D(relativeArcCentre, centre))

'''--- Output to svg format -------------------------------------------------------------------------- '''

outFile.write("""<svg height=\"%d\" width=\"%d\">
    """ %(centre.Y+radius+10, centre.X+radius+10))

''' Drawing ''' 
for i in range(len(itemValues)):
    #Centre Point 
    outFile.write("<path d=\"M%d,%d " %(centre.X, centre.Y))
    
    #Radius
    outFile.write("L%d,%d " %(points[i].X, points[i].Y))
    
    #Arc
    if itemValues[i] < math.pi:
        largeArcFlag = 0
    else:
        largeArcFlag = 1
    if i == len(itemValues) - 1:
        outFile.write("A%d,%d 0 %d,1 %d,%d " %(radius, radius, largeArcFlag, points[0].X, points[0].Y))
    else:
        outFile.write("A%d,%d 0 %d,1 %d,%d " %(radius, radius, largeArcFlag, points[i+1].X, points[i+1].Y))
    
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

''' Text '''
for i in range(len(itemValues)):
    #Choose text location
    outMax = 0.9
    outMin = 0.4
    if itemValues[i] < math.pi:
        outNess = outMax - (itemValues[i]/math.pi * (outMax-outMin))
    else:
        outNess = outMin
    textCentre = alongPoints2D(centre, arcCentres[i], outNess)
    
    #Taking default styles if not specified
    if 'font-family' not in dataObject.keys():
        fontFamily = defaultStyles['font-family']
    else:
        fontFamily = dataObject['font-family']
    if 'font-fill' not in dataObject.keys():
        fontFill = defaultStyles['font-fill']
    else:
        fontFill = dataObject['font-fill']
    if 'font-outline' not in dataObject.keys():
        fontOutline = defaultStyles['font-outline']
    else:
        fontOutline = dataObject['font-outline']
    if 'font-size' not in dataObject.keys():
        fontSize = radius/10
    else:
        fontSize = dataObject['font-size']
    if 'show-percent' not in dataObject.keys():
        displayText = str(dataObject['items'][i]['value'])
    elif dataObject['show-percent'] == True:
        displayText = "%0.1f" %(percentages[i]) + "%"
    else:
        displayText = str(dataObject['items'][i]['value'])
    outFile.write("""<text
        font-family = \"%s\"
        fill = \"%s\"
        stroke = \"%s\"
        font-size = \"%s\"
        text-anchor = \"middle\"
        x = \"%d\"
        y = \"%d\">%s
    </text>""" % (fontFamily, fontFill, fontOutline, fontSize, 
        textCentre.X, textCentre.Y, displayText))
outFile.write("\n</svg>")
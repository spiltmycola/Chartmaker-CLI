class Point2D:
    def __init__(self, xCoord, yCoord):
        self.X = xCoord
        self.Y = yCoord

    def __str__(self):
        return "self.X: %0.2f\nself.Y: %0.2f\n" % (self.X, self.Y)

#Performs vector addition
def vectorAdd2D(pointA, pointB):
    return Point2D(pointA.X + pointB.X, pointA.Y + pointB.Y)

#Finds point between two points, based on proximity to each one e.g. (A, B, 0.5) would be midpoint
def alongPoints2D(pointA, pointB, proportion):
    return Point2D(pointA.X*(1-proportion) + pointB.X*proportion, pointA.Y*(1-proportion) + pointB.Y*proportion)
from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


class ConvexHull(QObject):

    def __init__(self, outsidePts, rightMostIndex, leftMostIndex):
        super().__init__()
        self.outsidePts = outsidePts
        self.leftMostIndex = leftMostIndex
        self.rightMostIndex = rightMostIndex

    def getOutsidePts(self):
        return self.outsidePts

    def getRightMostIndex(self):
        return self.rightMostIndex

    def getLeftMostIndex(self):
        return self.leftMostIndex

    def getRightMostPoint(self):
        return self.outsidePts[self.rightMostIndex]

    def getLeftMostPoint(self):
        return self.outsidePts[self.leftMostIndex]

    def getPoint(self, i):
        return self.outsidePts[i]

    def getLength(self):
        return len(self.outsidePts)

    def getNext(self, i): # Clockwise
        return self.outsidePts[(i + 1) % len(self.outsidePts)]

    def getPrev(self, i): # Counterclockwise
        if i == 0:
            return self.outsidePts[len(self.outsidePts) - 1]
        else:
            return self.outsidePts[i - 1]

    def getNextIndex(self, i):
        val = ((i + 1) % len(self.outsidePts))
        return val

    def getPrevIndex(self, i):
        if i == 0:
            return len(self.outsidePts) - 1
        else:
            return i - 1

    def toString(self):
        return "Number of Points: " + str(len(self.outsidePts)) + "\nLeft most index: " + str(self.leftMostIndex) \
               + "\nRight most index: " + str(self.rightMostIndex) + "\n"

#
# This is the class you have to complete.
#
def calcSlope(rightPt, leftPt):
    x1 = rightPt.x()  # x of left end of tangent
    y1 = rightPt.y()  # y of left end of tangent
    x2 = leftPt.x()  # x of right end of tangent
    y2 = leftPt.y()  # y of right end of tangent
    return (y2 - y1) / (x2 - x1)

def findUpperTangent(leftHull, rightHull):
    lRightMostIndex = leftHull.getRightMostIndex()
    rLeftMostIndex = rightHull.getLeftMostIndex()
    rightMost = leftHull.getRightMostPoint()
    leftMost = rightHull.getLeftMostPoint()

    slope = calcSlope(rightMost, leftMost)  # O(1)
    done = False
    while not done:
        done = True
        isLUpperTang = False
        while not isLUpperTang:
            tempRight = leftHull.getPrev(lRightMostIndex)  # counterclockwise neighbor
            tempSlope = calcSlope(tempRight, leftMost)
            if tempSlope < slope:
                rightMost = tempRight
                slope = tempSlope
                lRightMostIndex = leftHull.getPrevIndex(lRightMostIndex)
                done = False
            else:
                isLUpperTang = True

        isRUpperTang = False
        while not isRUpperTang:
            tempLeft = rightHull.getNext(rLeftMostIndex)  # clockwise neighbor
            tempSlope = calcSlope(rightMost, tempLeft)
            if tempSlope > slope:
                leftMost = tempLeft
                slope = tempSlope
                rLeftMostIndex = rightHull.getNextIndex(rLeftMostIndex)
                done = False
            else:
                isRUpperTang = True

    return lRightMostIndex, rLeftMostIndex

def findLowerTangent(leftHull, rightHull):
    lRightMostIndex = leftHull.getRightMostIndex()
    rLeftMostIndex = rightHull.getLeftMostIndex()
    rightMost = leftHull.getRightMostPoint()
    leftMost = rightHull.getLeftMostPoint()

    slope = calcSlope(rightMost, leftMost)
    done = False
    while not done:
        done = True
        isLLowerTang = False
        while not isLLowerTang:
            tempRight = leftHull.getNext(lRightMostIndex)  # clockwise neighbor
            tempSlope = calcSlope(tempRight, leftMost)
            if tempSlope > slope:
                rightMost = tempRight
                slope = tempSlope
                lRightMostIndex = leftHull.getNextIndex(lRightMostIndex)
                done = False
            else:
                isLLowerTang = True

        isRLowerTang = False
        while not isRLowerTang:
            tempLeft = rightHull.getPrev(rLeftMostIndex)  # counterclockwise neighbor
            tempSlope = calcSlope(rightMost, tempLeft)
            if tempSlope < slope:
                leftMost = tempLeft
                slope = tempSlope
                rLeftMostIndex = rightHull.getPrevIndex(rLeftMostIndex)
                done = False
            else:
                isRLowerTang = True

    return lRightMostIndex, rLeftMostIndex


def findTangents(leftHull, rightHull):  # putting everything back together O(N)
    upperLeft, upperRight = findUpperTangent(leftHull, rightHull)
    lowerLeft, lowerRight = findLowerTangent(leftHull, rightHull)

    rightMostIndex = upperRight
    rightMostPoint = rightHull.getPoint(rightMostIndex)

    index = 0
    newHullArray = []
    start = 0
    while start <= upperLeft:  # adds left most point first and upper left last
        newHullArray.append(leftHull.getPoint(start))
        index = index + 1
        start = start + 1

    # add upper right first and stop right before adding lower right
    start = upperRight
    while start != lowerRight:
        newPoint = rightHull.getPoint(start)
        if newPoint.x() >= rightMostPoint.x():
            rightMostIndex = index
            rightMostPoint = newPoint

        newHullArray.append(newPoint)
        index = index + 1
        start = rightHull.getNextIndex(start)

    if lowerRight == upperRight:
        newHullArray.append(rightHull.getPoint(lowerRight))
        rightMostIndex = index
    elif start == lowerRight:
        newPoint = rightHull.getPoint(lowerRight)
        if newPoint.x() > rightMostPoint.x():
            rightMostIndex = index

        newHullArray.append(newPoint)

    # if start = 0 that means that the lowerleft is the same as the upperleft and so its already in there
    start = lowerLeft
    while start != 0:  # lower left gets added first
        newHullArray.append(leftHull.getPoint(start))
        start = leftHull.getNextIndex(start)

    newHull = ConvexHull(newHullArray, rightMostIndex, 0)
    return newHull


class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    def findPolygon(self, points):  # Total Time Complexity: O(logbase2 N)
        length = len(points)
        if length == 1:
            return ConvexHull(points, 0, 0)

        mid = length // 2
        leftHull = self.findPolygon(points[:mid])
        rightHull = self.findPolygon(points[mid:])

        if leftHull.getLength() == 1 and rightHull.getLength() == 1:
            newHullArray = [leftHull.getPoint(0), rightHull.getPoint(0)]
            return ConvexHull(newHullArray, 1, 0)
        elif leftHull.getLength() == 1 and rightHull.getLength() == 2:
            leftPoint1 = leftHull.getPoint(0)
            rightPoint1 = rightHull.getPoint(0)
            rightPoint2 = rightHull.getPoint(1)
            newHullArray = [leftPoint1]
            slope1 = calcSlope(leftPoint1, rightPoint1)
            slope2 = calcSlope(leftPoint1, rightPoint2)
            rightIndex = 2
            if slope1 > slope2:
                newHullArray.append(rightPoint1)
                newHullArray.append(rightPoint2)
            else:
                newHullArray.append(rightPoint2)
                newHullArray.append(rightPoint1)
                rightIndex = 1

            return ConvexHull(newHullArray, rightIndex, 0)

        newHull = findTangents(leftHull, rightHull)

        return newHull

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()

        def getX(point):
            return point.x()

        points.sort(key=getX)
        t2 = time.time()

        t3 = time.time()
        convexHull = self.findPolygon(points)
        pointsArray = convexHull.getOutsidePts()
        polygon = [QLineF(pointsArray[i], pointsArray[(i + 1) % len(pointsArray)]) for i in range(len(pointsArray))]
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))

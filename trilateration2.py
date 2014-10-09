import math
import simplevector

class TrilaterationCalculation():
	def __init__ (self):
		self.RADIUS_INCREMENT = 1.005
		self.DISTANCE_TRESHOLD = 0.1
		self.defaultUserCoordinate = {'x': -1, 'y': -1}
	
	def determineTrilateration(self, selection_list):
		circles = self.determineCircles(selection_list)
		userCoordinate = self.calculateUserCoordinates(circles)
		return userCoordinate
	
	def determineCircles(self, selection_list):
		circles = []
		for selection in selection_list:
			x = float(selection['node']['x'])/100.0
			y = float(selection['node']['y'])/100.0
			radius = float(selection.get('ap').get('distance'))
			circle = {}
			circle['x'] = x
			circle['y'] = y
			circle['radius'] = radius
			circles.append(circle)
		return circles
	
	def calculateUserCoordinates(self, circles):
		intersections = self.determineIntersections(circles[0], circles[1])
		if intersections is None:
			print "Bad data: No intersections found after 10 iterations"
			userCoordinate = self.defaultUserCoordinate
		else:
			intersection1 = {}
			intersection1['x'] = intersections[0][0]
			intersection1['y'] = intersections[0][1]
			intersection2 = {}
			intersection2['x'] = intersections[1][0]
			intersection2['y'] = intersections[1][1]
			userCoordinate = self.determineBestPoint(intersection1, intersection2, circles[2])
		return userCoordinate
	
	def determineIntersections(self, router1, router2):
		for x in range(0, 10): # Try 10 times
			intersections = self.calculateIntersections(router1, router2)
			if intersections is None:
				router1['radius'] = router1.get('radius') * self.RADIUS_INCREMENT
				router2['radius'] = router2.get('radius') * self.RADIUS_INCREMENT
			else:
				return intersections
		return None
					
	def calculateIntersections(self, router1, router2):
		x1 = router1.get('x')
		y1 = router1.get('y')
		x2 = router2.get('x')
		y2 = router2.get('y')
		
		radius1 = router1.get('radius')
		radius2 = router2.get('radius')
		
		vector1 = self.createVector(router1)
		vector2 = self.createVector(router2)
		
		distBtwRouter = (vector1 - vector2).magnitude
		heronRoot = ( (distBtwRouter + radius1 + radius2)*
					(-distBtwRouter + radius1 +radius2)*
					(distBtwRouter - radius1 + radius2)*
					(distBtwRouter + radius1 - radius2) )
		
		if(heronRoot > 0): # intersection exists
			heron = 0.25*math.sqrt(heronRoot)
			xbase = (0.5)*(x1+x2) + (0.5)*(x2-x1)*(radius1*radius1-radius2*radius2)/(distBtwRouter*distBtwRouter)
			xdiff = 2*(y2-y1)*heron/(distBtwRouter*distBtwRouter) 
			ybase = (0.5)*(y1+y2) + (0.5)*(y2-y1)*(radius1*radius1-radius2*radius2)/(distBtwRouter*distBtwRouter)
			ydiff = 2*(x2-x1)*heron/(distBtwRouter*distBtwRouter) 
			return (xbase+xdiff,ybase-ydiff),(xbase-xdiff,ybase+ydiff)
		else: # no intersection exists
			print "No intersection found"
			return None
	
	def determineBestPoint(self, intersection1, intersection2, router3):
		vector1 =  self.createVector(intersection1)
		vector2 =  self.createVector(intersection2)
		vector3 =  self.createVector(router3)
		
		distance1 = (vector3 - vector1).magnitude
		distance2 = (vector3 - vector2).magnitude
		
		radius = router3.get('radius')
		
		if( math.fabs(distance1 - radius) < math.fabs(distance2 - radius)):
			bestPoint = intersection1
			distance = distance1
		else:
			bestPoint = intersection2
			distance = distance2
		
		distDiff = math.fabs(distance - radius)
		if distDiff < distance * self.DISTANCE_TRESHOLD: # if intersection lies within accepted threshold
			return bestPoint
		else:
			print "Both intersections not within accepted threshold"
			return self.defaultUserCoordinate
		
	def createVector(self, point):
		x = point.get('x')
		y = point.get('y')
		return simplevector.Vector2d(x,y)
	
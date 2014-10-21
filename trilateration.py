import math
import simplevector

class TrilaterationCalculation():
	def __init__ (self):
		### CONSTANTS ###
		self.RADIUS_INCREMENT = 1.4
		self.DISTANCE_THRESHOLD = 0.6
		self.NUMBER_OF_ITERATIONS = 6
		self.TOLERANCE = 0.5
		self.DEFAULT_COORDINATES = simplevector.Vector2d(-1,-1)
		self.STOP_ITERATION = -1
		
		### CLASS ATTRIBUTES ###
		self.savedCircles = []
		self.iterationNum = 0
		self.intersectedCircles = {}
		
	##########################################
	# Methods used by Wifi class
	##########################################
	
	def determineTrilateration(self, selection_list):
		circles = self.determineCircles(selection_list)
		userLocation = self.findAllIntersections(circles)
		return userLocation
	
	##########################################
	# Helper Functions
	##########################################
	
	def determineCircles(self, selection_list):
		circles = []
		for data in selection_list:
			circle = self.buildCircle(data)
			circles.append(circle)
		return circles
	
	def buildCircle(self, data):
		circle = {}
		
		coordTuple = self.convertCoordToMeters(data.get('node'))
		radius = float(data.get('ap').get('distance'))
		name = data.get('ap').get('address')
		
		circle['coords'] = simplevector.Vector2d(coordTuple[0], coordTuple[1])
		circle['radius'] = radius
		circle['macAddr'] = name
		return circle
	
	def convertCoordToMeters(self, coordinates):
		x = float(coordinates.get('x'))/100.0
		y = float(coordinates.get('y'))/100.0
		return (x,y)
	
	def findAllIntersections(self, circles):
		intersectionPairList = []
		self.intersectedCircles = {}
		passCount = 0
		index = 0
		for j in range(0, len(circles)-1):
			for k in range(j+1, len(circles)):
				intersectionPair = self.find2CirclesIntersections(j, k, circles)
				if intersectionPair is not None:
					intersectionPairList.append(intersectionPair)
					passCount += 1
					if passCount == 1:
						index = self.determineIndexOfUnusedCircle(j, k)
		if len(intersectionPairList) == 0:
			print "No intersections found"
			return self.DEFAULT_COORDINATES
		elif passCount == 1:
			return self.determineBestPoint(intersectionPairList[0],circles[index])
		else:
			return self.determineCoordinatesInAllCircles(intersectionPairList)
	
	def find2CirclesIntersections(self, index1, index2, circles):
		circle1 = circles[index1]
		circle2 = circles[index2]
		radius1 = circle1.get('radius')
		radius2 = circle2.get('radius')
		vector1 = circle1.get('coords')
		vector2 = circle2.get('coords')
		
		for x in range(0, self.NUMBER_OF_ITERATIONS):
			intersectionPair = self.computeIntersection(vector1, radius1, vector2, radius2)
			if intersectionPair == self.STOP_ITERATION:
				print "Iteration stopped: Circles engulfing one another"
				break
			elif intersectionPair is None:
				radius1 *= self.RADIUS_INCREMENT
				radius2 *= self.RADIUS_INCREMENT
			else:
				self.updateIntersectedCircles(circle1, radius1, circle2, radius2)
				return intersectionPair
		return None
	
	def updateIntersectedCircles(self, circle1, radius1, circle2, radius2):
		isFound = self.intersectedCircles.get(circle1.get('macAddr'))
		if isFound is None:
			self.intersectedCircles[circle1.get('macAddr')] = circle1
		elif isFound.get('radius') < radius1:
			isFound['radius'] = radius1
		isFound = self.intersectedCircles.get(circle2.get('macAddr'))
		if isFound is None:
			self.intersectedCircles[circle2.get('macAddr')] = circle2
		elif isFound.get('radius') < radius2:
			isFound['radius'] = radius2
		
	
	def computeIntersection(self, vector1, radius1, vector2, radius2):
		results = []
		distance = (vector2 - vector1).magnitude
		# Circles do not touch
		if(distance > (radius1 + radius2)):
			return None
		# Circles contained within one another
		elif(distance < math.fabs(radius1 - radius2)):
			return self.STOP_ITERATION
		else:
			a = (math.pow(radius1,2)-math.pow(radius2,2)+math.pow(distance,2))/(2*distance)
			h = math.sqrt(math.pow(radius1,2) - math.pow(a,2))
			p3 = vector1 + (a*(vector2-vector1)/distance)
	
			x3_1 = p3[0] + (h*(vector2[1]-vector1[1])/distance)
			y3_1 = p3[1] - (h*(vector2[0]-vector1[0])/distance)
	
			x3_2 = p3[0] - (h*(vector2[1]-vector1[1])/distance)
			y3_2 = p3[1] + (h*(vector2[0]-vector1[0])/distance)
	
			intersection1 = simplevector.Vector2d(x3_1,y3_1)
			intersection2 = simplevector.Vector2d(x3_2,y3_2)
	
			if intersection1 == intersection2:
				results.append(intersection1)
			else:
				results.append(intersection1)
				results.append(intersection2)
		return results
	
	def determineIndexOfUnusedCircle(self, j, k):
		if j == 1: return 0
		elif k == 1: return 2
		else: return 1
	
	def determineCoordinatesInAllCircles(self, intersectionPairList):
		coordinates = []
		for coord_tuple in intersectionPairList:
			for coord in coord_tuple:
				count = 0
				for key in self.intersectedCircles:
					circle = self.intersectedCircles.get(key)
					if self.determineWithinCircle(circle.get('coords'),
												  float(circle.get('radius')),
												  float(coord[0]),
												  float(coord[1])):
						count += 1
					if count >= len(self.intersectedCircles) - 1:
						coordinates.append(coord)
						break
		return self.determineLocation(coordinates)
	
	def determineLocation(self, coordinates):
		sum_x = 0
		sum_y = 0
		if len(coordinates) == 0:
			print "Unable to determine user coordinate"
			return self.DEFAULT_COORDINATES

		for coordinate in coordinates:
			sum_x += coordinate[0]
			sum_y += coordinate[1]
	
		mid_x = sum_x/len(coordinates)
		mid_y = sum_y/len(coordinates)
	
		return simplevector.Vector2d(mid_x*100,mid_y*100)

	def determineWithinCircle(self, vector, r, x1, y1):
		x = vector[0]
		y = vector[1]
		return (math.pow(x-x1,2) + math.pow(y-y1,2) - math.pow(r,2)) <= self.TOLERANCE
	
	def determineBestPoint(self, found_coordinates, router3):
		if len(found_coordinates) == 1:
			return found_coordinates[0]
		
		vector1 = found_coordinates[0]
		vector2 = found_coordinates[1]
		vector3 =  self.createVector(router3)
		
		distance1 = (vector3 - vector1).magnitude
		distance2 = (vector3 - vector2).magnitude
		
		radius = router3.get('radius')
		
		if( math.fabs(distance1 - radius) < math.fabs(distance2 - radius)):
			bestPoint = vector1
			distance = distance1
		else:
			bestPoint = vector2
			distance = distance2
		
		distDiff = math.fabs(distance - radius)
		if distDiff < distance * self.DISTANCE_THRESHOLD: # if intersection lies within accepted threshold
			bestPoint[0] *= 100
			bestPoint[1] *= 100
			return bestPoint
		else:
			print "Both intersections not within accepted threshold"
			return self.DEFAULT_COORDINATES

	def createVector(self, point):
		x = point.get('x')
		y = point.get('y')
		return simplevector.Vector2d(x,y)
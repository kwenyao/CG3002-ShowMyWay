import math
import simplevector

class TrilaterationCalculation():
	def __init__ (self):
		self.RADIUS_INCREMENT = 1.4
		self.DISTANCE_THRESHOLD = 0.6
		self.defaultUserCoordinate = {'x': -1, 'y': -1}

	def cc_intersect(self, p1, r1, p2, r2):
	
		results = []
		distance = (p2 - p1).magnitude
		# print "distance between 2 points: " + str(distance)
		if(distance > (r1 + r2)):
			# print "circles are separate"
			# results.append("circles are separate")
			return None
		elif(distance < math.fabs(r1 - r2)):
			# print "one circle is contained within the other"
			# results.append("one circle is contained within the other")
			return None
		elif(distance == 0 and (r1 == r2)):
			# print "circles are exactly identical in position and radius"
			# results.append("circles are exactly identical in position and radius")
			return None
		else:
			a = (math.pow(r1,2)-math.pow(r2,2)+math.pow(distance,2))/(2*distance)
			# print str(math.pow(r1,2) - math.pow(a,2))
			h = math.sqrt(math.pow(r1,2) - math.pow(a,2))
			p3 = p1 + (a*(p2-p1)/distance)
	
			x3_1 = p3[0] + (h*(p2[1]-p1[1])/distance)
			y3_1 = p3[1] - (h*(p2[0]-p1[0])/distance)
	
			x3_2 = p3[0] - (h*(p2[1]-p1[1])/distance)
			y3_2 = p3[1] + (h*(p2[0]-p1[0])/distance)
	
			p4_1 = simplevector.Vector2d(x3_1,y3_1)
			p4_2 = simplevector.Vector2d(x3_2,y3_2)
	
			if p4_1 == p4_2:
				results.append(p4_1)
			else:
				results.append(p4_1)
				results.append(p4_2)
		return results
	
	def determineWithinCircle(self, x, y, r, x_1, y_1):
		return (math.pow(x-x_1,2) + math.pow(y-y_1,2) - math.pow(r,2)) <= 0.2 #tolerance
	
	def determineCoordinatesInAllCircles(self, list_of_coordinates,circles):
		coordinates = []
		for coord_tuple in list_of_coordinates:
			for coord in coord_tuple:
				count = 0
				for circle in circles:
					# print "Circle x: " + str(circle['x'])
					# print "Circle y: " + str(circle['y'])
					# print "Circle Dist: " + str(circle['dist'])
					# print "Coord a: " + str(coord[0])
					# print "Coord b: " + str(coord[1])
					if self.determineWithinCircle(float(circle['x']),float(circle['y']),float(circle['dist']),float(coord[0]),float(coord[1])):
						count += 1
					# print count
					if count >= len(circles):
						coordinates.append(coord)
						break
					
		return coordinates
	
	def determineIntersections(self, circles):
		found_coordinates = []
		for j in range(0, len(circles)-1):
			for k in range(j+1, len(circles)):
				failing = True
				increase_attempt = 0
				coordinates = []
				a_x = circles[j]['x']
				a_y = circles[j]['y']
				dist_a = circles[j]['dist']
				pA = simplevector.Vector2d(a_x,a_y)
	
				b_x = circles[k]['x']
				b_y = circles[k]['y']
				dist_b = circles[k]['dist']
				pB = simplevector.Vector2d(b_x,b_y)
				
				while failing and increase_attempt < 10:
					coordinates = self.cc_intersect(pA, dist_a, pB, dist_b)
					if coordinates == None:
						dist_a *= self.RADIUS_INCREMENT
						# print "distance A: " + str(dist_a)
						dist_b *= self.RADIUS_INCREMENT
						# print "distance B: " + str(dist_b)
						increase_attempt += 1
						# print "increase attempt :" + str(increase_attempt)
						continue
					else:
						found_coordinates.append(coordinates)
						failing = False
						circles[k]['dist'] = dist_b
						circles[j]['dist'] = dist_a
				if failing == True:
					print "increase attempt failed!"

		return self.determineCoordinatesInAllCircles(found_coordinates, circles)
	
	def determineCircles(self, selection_list):
		circles = []
		for selection in selection_list:
			x = float(selection['node']['x'])/100.0
			y = float(selection['node']['y'])/100.0
			dist = float(selection['ap']['distance'])
			circle = {}
			circle['x'] = x
			circle['y'] = y
			circle['dist'] = dist
			circles.append(circle)
		return circles
	
	def determineLocation(self, coordinates):
		sum_x = 0
		sum_y = 0
		if len(coordinates) == 0:
			print "Unable to determine user coordinate"
			return simplevector.Vector2d(self.defaultUserCoordinate['x'], self.defaultUserCoordinate['y'])

		for coordinate in coordinates:
			sum_x += coordinate[0]
			sum_y += coordinate[1]
	
		mid_x = sum_x/len(coordinates)
		mid_y = sum_y/len(coordinates)
	
		return simplevector.Vector2d(mid_x*100,mid_y*100)

	def determineTrilateration(self, selection_list):
		circles = self.determineCircles(selection_list)
		# print "circle: "
		# print circles
		localization_coordinates = self.determineIntersections(circles)
		# print "localization_coordinates: "
		# print localization_coordinates
		userLocation = self.determineLocation(localization_coordinates)
		return userLocation

import math
import simplevector

class TrilaterationCalculation():
	def cc_intersect(self, p1, r1, p2, r2):
	
		results = []
		distance = (p2 - p1).magnitude
	
		if(distance > (r1 + r2)):
			#circles are separate
			results.append("circles are separate")
			#return results
		elif(distance < math.fabs(r1 - r2)):
			#one circle is contained within the other
			results.append("one circle is contained within the other")
			#return results
		elif(distance == 0 and (r1 == r2)):
			#circles are exactly identical in position and radius
			results.append("circles are exactly identical in position and radius")
			#return results
		else:
			a = (math.pow(r1,2)-math.pow(r2,2)+math.pow(distance,2))/(2*distance)
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
					if self.determineWithinCircle(circle['x'],circle['y'],circle['dist'],coord[0],coord[1]):
						count += 1
					if count >= len(circles):
						coordinates.append(coord)
						break
					
		return coordinates
	
	def determineIntersectionCoordinates(self, circles):
		found_coordinates = []
		for j in range(0, len(circles)-1):
			circleA = circles[j]
			for k in range(j+1, len(circles)):
				circleB = circles[k]
				coordinates = []
				a_x = circleA['x']
				a_y = circleA['y']
				dist_a = circleA['dist']
				pA = simplevector.Vector2d(a_x,a_y)
	
				b_x = circleB['x']
				b_y = circleB['y']
				dist_b = circleB['dist']
				pB = simplevector.Vector2d(b_x,b_y)
	
				coordinates = self.cc_intersect(pA, dist_a, pB, dist_b)
				found_coordinates.append(coordinates)
	
		return found_coordinates
	
	def determineCircles(self, selection_list):
		circles = []
		for selection in selection_list:
			x = float(selection['node']['x'])
			y = float(selection['node']['y'])
			dist = selection['ap']['distance']
			circle = {}
			circle['x'] = x
			circle['y'] = y
			circle['dist'] = dist
			circles.append(circle)
		return circles
	
	def determineLocation(self, coordinates):
		sum_x = 0
		sum_y = 0
		for coordinate in coordinates:
			sum_x += coordinate[0]
			sum_y += coordinate[1]
	
		mid_x = sum_x/len(coordinates)
		mid_y = sum_y/len(coordinates)
	
		return simplevector.Vector2d(mid_x,mid_y)

import math
# import vector
import simplevector

# class positiveinfinity:
# 	"""Positive Infinity, a value greater then any other value except itself. 
#    	Only one instance of this class is needed, instantiated in this module as 
# 	PosInf."""
# 	def __cmp__(self, other):
# 		if other.__class__ == self.__class__:
# 			return 0
# 		else:
# 			return 1

#         def __hash__(self):
#             return 0

# 	def __repr__(self):
# 		return str(__name__)+".PosInf"
	
# 	def __str__(self):
# 		return "PosInf"
# # end class positiveinfinity

# class negativeinfinity:
# 	"""Negative Infinity, a value greater then any other value except itself. 
#    	Only one instance of this class is needed, instantiated in this module as 
# 	NegInf."""
# 	def __cmp__(self, other):
# 		if other.__class__ == self.__class__:
# 			return 0
# 		else: 
# 			return -1

#         def __hash__(self):
#             return 1

# 	def __repr__(self):
# 		return str(__name__)+".NegInf"
	
# 	def __str__(self):
# 		return "NegInf"
# # end class positiveinfinity


# #Positive infinity. This variable is an instance of positiveinfinity. 
# #No other instances need to be created.  
# PosInf = positiveinfinity()

# #Negative infinity. This variable is an instance of negativeinfinity. 
# #No other instances need to be created.  
# NegInf = negativeinfinity()

# # The default tolerance, used when no tolerance argument is given
# # to the comparion functions, or when "Default" is passed.  
# default_tol = 1e-6

# def tol_lt(a,b,tol="Default"):
# 	"""Tolerant less-than: return b-a>tol"""
# 	if tol=="Default":
# 		tol = default_tol
# 	if a == NegInf:
# 		return b != NegInf
# 	elif a == PosInf:
# 		return False
# 	elif b == PosInf:
# 		return a != PosInf
# 	elif b == NegInf:
# 		return False
# 	else:
# 		return b-a>tol

# def tol_gt(a,b,tol="Default"):
# 	"""Tolerant greater-than: return a-b>tol"""
# 	if tol=="Default":
# 		tol = default_tol
# 	if a == NegInf:
# 		return False
# 	elif a == PosInf:
# 		return b != PosInf
# 	elif b == NegInf:
# 		return a != NegInf
# 	elif b == PosInf:
# 		return False
# 	else:
# 		return a-b>tol

# def tol_eq(a,b,tol="Default"):
# 	"""Tolerant equal: return abs(a-b)<=tol"""
# 	if tol=="Default":
# 		tol = default_tol
# 	if a == PosInf: 
# 		return b == PosInf
# 	elif a == NegInf: 
# 		return b == NegInf
# 	elif b == PosInf: 
# 		return a == PosInf
# 	elif b == NegInf: 
# 		return a == NegInf
# 	else:
# 		return abs(a-b)<=tol

# def cc_int(p1, r1, p2, r2):
# 	"""
# 	Intersect circle (p1,r1) circle (p2,r2)
# 	where p1 and p2 are 2-vectors and r1 and r2 are scalars
# 	Returns a list of zero, one or two solution points.
# 	"""
# 	d = vector.norm(p2-p1)
# 	if not tol_gt(d, 0):
# 		return []
# 	u = ((r1*r1 - r2*r2)/d + d)/2
# 	if tol_lt(r1*r1, u*u):
# 		return []
#         elif r1*r1 < u*u:
#             v = 0.0
#         else:
#             v = math.sqrt(r1*r1 - u*u)
# 	s = (p2-p1) * u / d
# 	if tol_eq(vector.norm(s),0):
# 	        p3a = p1+vector.vector([p2[1]-p1[1],p1[0]-p2[0]])*r1/d
# 	        if tol_eq(r1/d,0):
#                     return [p3a]
#                 else:
#                     p3b = p1+vector.vector([p1[1]-p2[1],p2[0]-p1[0]])*r1/d
#                     return [p3a,p3b]
# 	else:
# 	        p3a = p1 + s + vector.vector([s[1], -s[0]]) * v / vector.norm(s) 
#                 if tol_eq(v / vector.norm(s),0):
#                     return [p3a]
#                 else:
#                     p3b = p1 + s + vector.vector([-s[1], s[0]]) * v / vector.norm(s)
#     	            return [p3a,p3b]


def cc_intersect(p1, r1, p2, r2):

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

def determineWithinCircle(x, y, r, x_1, y_1):
	return (math.pow(x-x_1,2) + math.pow(y-y_1,2) - math.pow(r,2)) <= 0.2 #tolerance

def determineCoordinatesInAllCircles(list_of_coordinates,circles):
	coordinates = []
	for coord_tuple in list_of_coordinates:
		for coord in coord_tuple:
			count = 0
			for circle in circles:
				if determineWithinCircle(circle['x'],circle['y'],circle['dist'],coord[0],coord[1]):
					count += 1
				if count >= len(circles):
					coordinates.append(coord)
					break
				
	return coordinates

def determineIntersectionCoordinates(circles):
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

			coordinates = cc_intersect(pA, dist_a, pB, dist_b)
			found_coordinates.append(coordinates)

	return found_coordinates

# def determineIntersectPoint(a_x, a_y, rad_a, b_x, b_y, rad_b):
# 	# (X - a_x)^2 + (Y - a_y)^2 = (dist_a)^2   ---- equation of circle
# 	results = []
# 	distance = math.sqrt(math.pow((a_x - b_x),2) + math.pow((a_y - b_y),2))
# 	#check case of intersection:
# 	#1)
# 	if(distance > (rad_a + rad_b)):
# 		#circles are separate
# 		results.append("circles are separate")
# 	elif(distance < math.fabs(rad_a - rad_b)):
# 		#one circle is contained within the other
# 		results.append("one circle is contained within the other")
# 	elif(distance == 0 and (rad_a == rad_b)):
# 		#circles are exactly identical in position and radius
# 		results.append("circles are exactly identical in position and radius")
# 	else:
# 		#at least 1 intersection exists
# 		if(a_x - b_x == 0):
# 			print "option a"
# 			# intersection is on a common Y-axis 
# 			k = math.pow(rad_b,2) - math.pow(rad_a,2) + math.pow(a_x,2) + math.pow(a_y,2) - math.pow(b_x,2) - math.pow(b_y,2)
# 			Y = 0.5*k/(a_y - b_y)
# 			A = 1
# 			B = -2*a_x
# 			C = math.pow(a_y,2) + math.pow(a_x,2) - math.pow(rad_a,2) + math.pow(Y,2) - 2*a_y*Y
# 			if(math.pow(B,2) - 4*A*C == 0):
# 				X = -B/(2*A)
# 				coordinate1 = (X,Y)
# 				results.append(coordinate1)
# 			elif(math.pow(B,2) - 4*A*C >= 0):
# 				X_1 = (-B - math.sqrt(math.pow(B,2) - 4*A*C))/(2*A)
# 				X_2 = (-B + math.sqrt(math.pow(B,2) - 4*A*C))/(2*A)
# 				coordinate1 = (float("{0:.2f}".format(X_1)),float("{0:.2f}".format(Y)))
# 				coordinate2 = (float("{0:.2f}".format(X_2)),float("{0:.2f}".format(Y)))
# 				results.append(coordinate1)
# 				results.append(coordinate2)

# 		elif(a_y - b_y==0):
# 			print "option b"
# 			# intersection is on a common X-axis 
# 			k = math.pow(rad_b,2) - math.pow(rad_a,2) + math.pow(a_x,2) + math.pow(a_y,2) - math.pow(b_x,2) - math.pow(b_y,2)
# 			X = 0.5*k/(a_x - b_x) 
# 			A = 1
# 			B = -2*a_y
# 			C = math.pow(a_y,2) + math.pow(a_x,2) - math.pow(rad_a,2) + math.pow(X,2) - 2*a_x*X 
# 			if(math.pow(B,2) - 4*A*C == 0):
# 				Y = -B/(2*A)
# 				coordinate1 = (X,Y)
# 				results.append(coordinate1)
# 			elif(math.pow(B,2) - 4*A*C >= 0):
# 				Y_1 = (-B - math.sqrt(math.pow(B,2) - 4*A*C))/(2*A)
# 				Y_2 = (-B + math.sqrt(math.pow(B,2) - 4*A*C))/(2*A)
# 				coordinate1 = (float("{0:.2f}".format(X)),float("{0:.2f}".format(Y_1)))
# 				coordinate2 = (float("{0:.2f}".format(X)),float("{0:.2f}".format(Y_2)))
# 				results.append(coordinate1)
# 				results.append(coordinate2)

# 		else:
# 			print "option c"
# 			k = math.pow(rad_b,2) - math.pow(rad_a,2) + math.pow(a_x,2) + math.pow(a_y,2) - math.pow(b_x,2) - math.pow(b_y,2)
# 			j = 0.5*k/(a_y - b_y)
# 			l = (a_x - b_x)/(a_y - b_y)


# 			A = 1 + math.pow(l,2)
# 			B = (2*a_y*l) - (2*a_x) - (2*j*l)
# 			C = math.pow(a_x,2) + math.pow(j,2) - (2*a_y*j) + math.pow(a_y,2) - rad_a
# 			print str(A) + "\n"
# 			print str(B) + "\n"
# 			print str(C) + "\n"
# 			print str(math.pow(B,2) - 4*A*C)
# 			if(math.pow(B,2) - 4*A*C == 0):
# 				print "option c-1"
# 				X_1 = -B/(2*A)
# 				Y_1 = j - (l*X_1)
# 				coordinate1 = (X_1,Y_1)
# 				results.append(coordinate1)

# 			elif(math.pow(B,2) - 4*A*C >= 0):
# 				print "option c-1"
# 				X_1 = (-B - math.sqrt(math.pow(B,2) - 4*A*C))/(2*A)
# 				X_2 = (-B + math.sqrt(math.pow(B,2) - 4*A*C))/(2*A)
# 				Y_1 = j - (l*X_1)
# 				Y_2 = j - (l*X_2)
# 				coordinate1 = (float("{0:.2f}".format(X_1)),float("{0:.2f}".format(Y_1)))
# 				coordinate2 = (float("{0:.2f}".format(X_2)),float("{0:.2f}".format(Y_2)))
# 				results.append(coordinate1)
# 				results.append(coordinate2)
# 	return results
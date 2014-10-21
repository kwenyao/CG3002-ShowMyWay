from heapq import *
import math

class getPath :
	def __init__(self, Map_nodes):
		self.graph_adjlist = []
		self.parent = {}
		self.dist = {}
		self.PQ = []
		for i in Map_nodes:
			self.graph_adjlist.append([])
			self.parent[i] = -1
			self.dist[i] = 1000000000000

	def formAdjlist(self, Map_nodes):
		for vertex, details in Map_nodes.iteritems():
		   # print vertex, details['x'], details['y'], details['linkTo']
		    neighbour_list = details['linkTo']
		    for neighbour in neighbour_list:
		    	weight = math.sqrt(((int(Map_nodes[neighbour]['y']) - int(details['y']))**2) + (int(Map_nodes[neighbour]['x']) - int(details['x']))**2)
		    	self.graph_adjlist[int(vertex)-1].append([weight, neighbour])

	def printAdjlist(self):
		for i in self.graph_adjlist:
			print i

	def shortestPath(self, start_point):
		self.dist[start_point] = 0
		first_node = (0,start_point)
		heappush(self.PQ, first_node)

		while (len(self.PQ) != 0):
			front = self.PQ[0];
			del self.PQ[0]
			# print front
			frontVertex = front[1];
			if (front[0] == self.dist[frontVertex]): 
				for neighbour in self.graph_adjlist[int(frontVertex)-1]:
					neighbourVertex = neighbour[1]
					neighbourWeight = neighbour[0]
					# print neighbourVertex
					# print self.dist[neighbourVertex],
					# print self.dist[frontVertex] ,
					# print neighbourWeight
					if (self.dist[neighbourVertex] > self.dist[frontVertex] + neighbourWeight):
						self.dist[neighbourVertex] = self.dist[frontVertex] + neighbourWeight
						self.parent[neighbourVertex] =  frontVertex
						new_entry = (self.dist[neighbourVertex], neighbourVertex)
						heappush(self.PQ, new_entry)
	
	def printParent(self):
		print self.parent

	def routeToTravel(self,start_point, end_point):
		route = [end_point,]
		while (self.parent[end_point] != start_point):
			end_point = self.parent[end_point]
			route.append(end_point)
		route.append(start_point)
		route.reverse()
		return route
		          


from Tkinter import *

class visualiseMap :
	def __init__(self,win_width, win_height):
		self.master = Tk()
		self.window = Canvas(self.master, width = win_width, height = win_height)
		self.window.pack()
		self.shrink = 5

	def addCoor(self,vertex,x,y):
		"This method adds a coordinate to our display map"
		self.window.create_oval(x/self.shrink-10,y/self.shrink+10 , x/self.shrink+10, y/self.shrink-10, fill = "red")
		self.window.create_text(x/self.shrink,y/self.shrink, text = vertex)

	def addPath(self, start_coor, stop_coor):
		"This method adds the lines for the edges"
		self.window.create_line(int(start_coor[0])/self.shrink, int(start_coor[1])/self.shrink, int(stop_coor[0])/self.shrink,int(stop_coor[1])/self.shrink, fill="black")
	def printMap(self):
			"This method prints out the display map to the console"
			mainloop()
	
	def addRoutePath(self, start_coor, stop_coor):
		"This method is to highlight the route to be taken as the shortest path"
		self.window.create_line(int(start_coor[0])/self.shrink, int(start_coor[1])/self.shrink, int(stop_coor[0])/self.shrink,int(stop_coor[1])/self.shrink, fill="red")

	def setMap(self, map_nodes, nature):
		"This method takes in the JSON format nodes and set the map"
		for k, v in map_nodes.iteritems():
			self.addCoor(k, int(v['x']), int(v['y']))
			start_point = [int(v['x']), int(v['y'])]
			end_point = []
			if v.has_key('linkTo') :
				for e in v['linkTo']:
					if map_nodes.has_key(e):
						end_point = [int(map_nodes[e]['x']), int(map_nodes[e]['y'])]
						if nature == 0 :
							self.addPath(start_point,end_point)
						else :
							self.addRoutePath(start_point,end_point)

	def getRouteNodes(self, map_nodes, route):
		"This method takes in the vertices required for the shortest path and return a JSON format data structure"
		route_nodes = {}
		for i in range(len(route)):
			route_nodes[route[i]] = map_nodes[route[i]]
			if i != len(route)-1 :
				route_nodes[route[i]]['linkTo'] = [route[i+1]]
			else :
				del route_nodes[route[i]]['linkTo']
		return route_nodes


	



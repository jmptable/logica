import math

# check if a pt is on an objects (Image)
def collide(x, y, objects, ignored=[]):
	for ob in objects:
		if ob.solid and not ob in ignored:
			left = ob.x
			right = ob.x + ob.image.width
			top = ob.y
			bottom = ob.y + ob.image.height
			
			if x >= left and x < right and y >= top and y < bottom:
				return ob
	
	return None
	
def isPassable(x, y, board, ignored=[], size=1):
	if not (x >= 0 and y >= 0 and x < board.width and y < board.height):
		return False
	
	if size > 1:
		for xOff in range(-size, size+1):
			for yOff in range(-size, size+1):
				if(not collide(x+xOff, y+yOff, board.parts, ignored) == None):
					return False
		
		return True
	else:
		return collide(x, y, board.parts) == None

class SearchNode:
        def __init__(self, state, parent, cost):
                self.state = state
                self.parent = parent
                self.cost = cost

        def getChildren(self):
                return []

        def getPath(self):
                out = []
                current = self
                while current is not None:
                        out.append(current.state)
                        current = current.parent
                return out[::-1]

class CircuitSearchNode(SearchNode):
	def __init__(self, board, ignored, state, parent, cost, size=1):
		self.size = size
		self.board = board
		self.ignored = ignored
		SearchNode.__init__(self,state,parent,cost)

	def getChildren(self):
		x, y = self.state
		out = []
		for (dx,dy) in [(1,0),(0,1),(-1,0),(0,-1)]:
			nx,ny = x+dx,y+dy
			
			if isPassable(nx, ny, self.board, self.ignored, self.size):
				out.append(CircuitSearchNode(self.board,self.ignored,(nx,ny),self,self.cost+1.0))
		for (dx,dy) in [(1,1),(1,-1),(-1,1),(-1,-1)]:
			if all(isPassable(x, y, self.board, self.ignored, self.size) for x, y in [(x+dx,y),(x,y+dy),(x+dx,y+dy)]):
				out.append(CircuitSearchNode(self.board,self.ignored,(x+dx,y+dy),self,self.cost+2**0.5))
		return out

def ucSearch(startNode, goalTest, heuristic=lambda s: 0):
	if goalTest(startNode.state):
		return startNode.getPath()
	agenda = [(startNode,startNode.cost+heuristic(startNode.state))]
	expanded = set()
	while len(agenda) > 0:
		agenda.sort(key=lambda n: n[1])
		node,priority = agenda.pop(0)
		if node.state not in expanded:
			expanded.add(node.state)
			if len(expanded)%10==0: print "Expanded",len(expanded),"states"
			if goalTest(node.state):
				print "Expanded",len(expanded),"states"
				return node.getPath()
			for child in node.getChildren():
				if child.state not in expanded:
					agenda.append((child,child.cost+heuristic(child.state)))
	print "Failed: Expanded",len(expanded),"states"
	return None
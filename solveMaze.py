import math

# Used for keeping track of the nodes to visit
class Node:
	def __init__(self, name, x, y):
		self.name = name
		self.x = x
		self.y = y
		self.visited = False

# Used for evaluating all of the neighbours added into the search 
# during the initial maze exploration
# For shortest paths
class Neighbour:
	def __init__(self, x, y, score, gScore):
		self.x = x
		self.y = y
		self.score = score
		self.gScore = gScore

# Return matching node by name
def getNode(name, nodes):
	for node in nodes:
		if node.name == name:
			return node

# Gets the maze from "maze.txt"
# Returns the maze as a 2D List
def getMaze():
	maze = []

	fname = "maze.txt"
	with open(fname) as f:
		content = f.readlines()
		for item in content:
	    		line = list(item.strip())
	    		maze.append(line)

	return maze

# Gets all of the nodes from the maze
# Returns a list of Node objects
def getNodes(maze):
	nodes = []
	for x, row in enumerate(maze):
		for y, space in enumerate(row):
			if space != '#' and space != '.':
				node = Node(space, x, y)
				nodes.append(node)

	return nodes

# Calculated the coordinate distance between two points
# Used for the heuristic calculation during A*
def distCalc(x, y, node):
	return math.sqrt(math.pow(node.x - x, 2) + math.pow(node.y - y, 2))	

# Calculates the best node candidate to search for next
# by using the heuristic distance calculation
def bestNodeEstimate(current, nodes):
	bestScore = None
	bestNode = None

	for node in nodes:
		# Only test if the node hasn't been visited yet
		if node.visited != True:
			distEstimate = distCalc(current.x, current.y, node)
			if bestScore == None or bestScore > distEstimate:
				bestScore = distEstimate
				bestNode = node

	return bestNode

# Runs the A* search algorithm to find all of the distances from the starting 
# node to the other nodes in the maze
def findShortestPaths(start, nodes, maze):
	adjacencyNodes = [[None for x in nodes] for x in nodes]
	nodesToVisit = len(nodes) - 1

	# Initialize starting node 
	print "Path taken:"
	print start.name,
	start.visited = True

	i = 0
	while nodesToVisit > 0:
		adjacencyNodes[int(start.name)][int(start.name)] = 0

		# Keeps track of visited maze locations as well as
		# neighbours that are to be consider
		visited = []
		closedSet = []
		openSet = []

		# Find the next node to search for based on heuristic
		goal = bestNodeEstimate(start, nodes);

		# Initialize g-scores
		gScore = []
		for x in maze:
			row = []
			for y in x:
				val = None
				row.append(val)
			gScore.append(row)

		gScore[start.x][start.y] = 0

		# Initialize f-scores
		fScore = []
		for x in maze:
			row = []
			for y in x:
				val = None
				row.append(val)
			fScore.append(row)		

		fScore[start.x][start.y] = distCalc(start.x, start.y, goal)

		openSet.append(Neighbour(start.x, start.y, fScore[start.x][start.y], 0))
		closedSet.append((start.x, start.y))
		
		# Search until you find the goal node
		while len(openSet) > 0:
			nextNeighbourToVisit = None

			# Visit the neigh with the lowest f(x) value next
			for x in openSet:
				if nextNeighbourToVisit == None or x.score < nextNeighbourToVisit.score:
					nextNeighbourToVisit = x

			posX = nextNeighbourToVisit.x
			posY = nextNeighbourToVisit.y

			# Update sets
			closedSet.remove((posX, posY))
			visited.append((posX, posY))				
			openSet.remove(nextNeighbourToVisit)

			# Check if we find the goal and update the adjacency matrix
        		if maze[posX][posY] == goal.name:
        			print "-> " + goal.name,
        			adjacencyNodes[int(start.name)][int(goal.name)] = nextNeighbourToVisit.gScore
        			adjacencyNodes[int(goal.name)][int(start.name)] = nextNeighbourToVisit.gScore
        			nodesToVisit -= 1   	
        			i += nextNeighbourToVisit.gScore
        			start = goal
        			goal.visited = True
        			break

        	# Otherwise add neighbours into next nodes to visit 
        		for x, y in [(posX-1, posY), (posX+1, posY), (posX, posY-1), (posX, posY+1)]:
        			#print "checking " + str(x) + " " + str(y) + " which has " + maze[x][y]
        			if maze[x][y] == '#' or (x, y) in closedSet or (x, y) in visited:
        				continue
        			else:
					openSet.append(Neighbour(x, y, nextNeighbourToVisit.gScore + distCalc(x, y, goal), nextNeighbourToVisit.gScore+1))
					closedSet.append((x, y))

			
	print ""
	print "Total steps: " + str(i)

	return adjacencyNodes
	
# Run 
def main():
	start = raw_input()
	maze = getMaze()
	nodes = getNodes(maze)
	startNode = getNode(start, nodes)
	adjacencyNodes = findShortestPaths(startNode, nodes, maze)

# Run main function
main()
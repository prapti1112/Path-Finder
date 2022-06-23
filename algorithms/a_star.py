import node

class A_star:
    def __init__(self, start, goal) -> None:
        print("Hello there from A* solver")
        self.start = start
        self.goal = goal
        self.open = []
        self.closed = []
    
    def assignHeuristics(self):
        '''
        Assigns the inintial hueristic values. Initial h, g = infinity except for the start and goal positions.
        '''
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                self.map[x][y].g = float('inf')
                self.map[x][y].h = float('inf')
                self.map[x][y].parent = None
        
                print(f"{self.map[x][y]}, G = {self.map[x][y].g}, H = {self.map[x][y].h}")
        
        startNode = self.map[self.start[0]][self.start[1]]

        startNode.g, startNode.h = 0, ((self.start[0] - self.goal[0])**2 + (self.start[1] - self.goal[1])**2)**0.5
        self.map[self.goal[0]][self.goal[1]].h = 0

    def getNeighbours(self, node):
        ''' Returns the unoccupied neighbours of a given node
        @param: node - current node whose neighbours are to be found
        '''
        neighbors = []
        x, y = node.x, node.y
        
        possible_neighbours = [[x + i_x, y + i_y] for i_x in [-1, 0, 1] for i_y in [-1, 0, 1] if (x + i_x) < len(self.map[0]) and (y + i_y) < len(self.map)]
        possible_neighbours.remove([x, y])
        
        print(f"Possible neighbours: {possible_neighbours}")
        for n in possible_neighbours:
            if self.map[n[0]][n[1]].status != "obstacle":
                self.map[n[0]][n[1]].status = "visited"
                neighbors.append(self.map[n[0]][n[1]])
        
        return neighbors

    def calculateCost(self, currentNode):
        ''' Calculates both the heuristic and cost value for the current node being explored
        @param: currentNode - the node being currently explored
        '''
        if currentNode.x == self.start[0] and currentNode.y == self.start[1]:
            currentNode.g = 0
        else:
            currentNode.g = currentNode.parent.g + 1
        currentNode.h = ((currentNode.x - self.goal[0])**2 + (currentNode.y - self.goal[1])**2)**0.5

    def getPath(self, map, start, goal):
        ''' Finds the path after solving using A* algorithms
        @param: map - A map representing current situation
        @param: start - start coordinate  of the robot
        @param: goal - goal coordinate to be reached
        '''
        self.map, self.start, self.goal = map, start, goal

        self.assignHeuristics()

        self.open.append(self.map[self.start[0]][self.start[1]])

        while len(self.open) != 0:
            currentNode = sorted(self.open, key = lambda node: (node.g + node.h))[0]
            print(f"Current Node: {currentNode}")

            if currentNode == self.map[self.goal[0]][self.goal[1]]:
                print("Path Found....")
                return [self.closed, self.map]
            
            for neighbour in self.getNeighbours(currentNode):
                print(f"({neighbour.x}, {neighbour.y})", end="  ")
                if neighbour not in self.closed and neighbour not in self.open:
                    neighbour.parent = currentNode
                    self.calculateCost(neighbour)
                    self.open.append(neighbour)
                elif (neighbour.g + neighbour.h) > (currentNode.g + 1 + currentNode.h) and neighbour != self.map[self.start[0]][self.start[1]]:
                    neighbour.parent = currentNode
                    self.calculateCost(neighbour)

                    if neighbour in self.closed:
                        self.closed.remove(neighbour)
                        self.open.append(neighbour)

            self.closed.append(currentNode)
            self.open.remove(currentNode)

        print("No path found....")
        return []
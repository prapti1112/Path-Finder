from math import sqrt
import random
from time import sleep
import node

class RRT:
    def __init__(self, start = [], goal = [], randomNodeDistanceLimit = 6, cellCount = 20) -> None:
        print("Hello from RRT")
        self.start = start
        self.goal = goal
        self.limit = randomNodeDistanceLimit
        self.open = []
        self.cellCount = cellCount
        self.iterations = 100
    

    def recountPath(self):
        ''' Reconstructs the path from the graph nodes available
        '''
        pathPositionNode = self.map[self.goal[0]][self.goal[1]]
        print("Current path:")
        while pathPositionNode != self.map[self.start[0]][self.start[1]]:
            print(f"{pathPositionNode}, {pathPositionNode.__dict__.keys()}")
        #     self.path.append(pathPosition)
            pathPositionNode = self.map[pathPositionNode.x][pathPositionNode.y].parent
        #     pathPositionNode
        # self.path.reverse()


    def distance(self, point1, point2):
        ''' Helper function that calculates euclidiean distance between point1 and point2
        '''
        return sqrt(( ( point1[0] - point2[0] )**2 + ( point1[1] - point2[1] )**2 ))


    def getNearestNeighbour(self, current):
        ''' Helper function to fint the neareest neighbour of a given node
        @param: current - The node whose neighbour is to be found
        '''
        neighbour = sorted([[self.distance((node.x, node.y), current), node.x, node.y] for node in self.open], key=lambda x: x[0])[0][1:]
        print(f"Neighbour found: {neighbour}")
        return neighbour
    
    def pathIsObstructed(self, destination, neighbour):
        ''' Checks if the straight line path between the destination node and nearest neighbour node has any obstabcles. This is done by finding the parameters of a line(slope, intercept) of the line joining destination and neighbour and checking if any one of the nodes in that path are an obstacle
        @param: destination - New destination node to be added to the graph
        @param: neighbour - node in the open list closest to the destination node
        '''
        print(f"Destination: {destination} Neighbour: {neighbour}")
        slope = float('inf') if destination[0] == neighbour[0] else ( (destination[1] - neighbour[1]) / (destination[0] - neighbour[0]) )
        
        if slope == float('inf'):
            print("Straight line detected")
            for y in range(min(destination[1], neighbour[1]), max(destination[1], neighbour[1])+1 ):
                print(f"Checking for obstacle at ({int(destination[0])}, {int(y)})")
                if self.map[int(destination[0])][int(y)].status == "obstacle":
                    return True
        else:
            print("Line with finite slope and intercept detected")
            intercept = neighbour[1] - slope * neighbour[0]
            for x in range(min(destination[0], neighbour[0])+1, max(destination[0], neighbour[0])+1):
                y = int(slope * x + intercept)
                print(f"Checking for obstacle at ({x}, {y})")
                if self.map[x][y].status == "obstacle":
                    return True
        
        return False


    def getDestination(self, current, neighbour):
        '''Gets the coordinates of a point on the line joining current node and neighbour node with distance along the line equal to the limit(default limit = 6)
        @param: current - The current randomly sampled node
        @param: neighbour - The nearest neighbour found from the already explored tree
        '''
        if self.distance(current, neighbour) < self.limit:
            return current
        
        destination = []
        # For info on calculations check: https://www.physicsforums.com/threads/formula-for-finding-point-on-a-line-given-distance-along-a-line.419561/#post-2822353
        slope = float('inf') if current[0] == neighbour[0] else ( (current[1] - neighbour[1]) / (current[0] - neighbour[0]) )
        x_possible = [int(neighbour[0] + (self.limit / sqrt(1 + slope**2))), int(neighbour[0] - (self.limit / sqrt(1 + slope**2)))]
        destinationX = int(x_possible[0]) if min(current[0], neighbour[0]) < x_possible[0] < max(current[0], neighbour[0]) else int(x_possible[1])
        destination.append( destinationX )
        multiplier = (current[1] - neighbour[1])/(abs(current[1] - neighbour[1]))
        destination.append( neighbour[1] + multiplier*self.limit if slope == float('inf') else int(neighbour[1] - slope*(neighbour[0] - destinationX)) )
        print(f"Destination: {destination}")

        return destination
    

    def getPath(self, map, startNode = None, goalNode = None):
        ''' Returns the path found by the RRT algorithm alond with the current version of the map
        @param: map - The initial map
        @param: startNode - start location for the path finder
        @param: goalNode - end location for the path finder
        '''
        self.path = []

        self.map = map
        if startNode != None:
            self.start = startNode
        if goalNode != None:
            self.goal = goalNode

        self.open.append(self.map[self.start[0]][self.start[1]])
        current = [random.randint(0, self.cellCount-1), random.randint(0, self.cellCount-1)]
        nearestNeighbor = self.getNearestNeighbour(current)

        for _ in range(self.iterations):
            destination = self.getDestination(current, nearestNeighbor)

            if destination == nearestNeighbor:
                continue

            if self.pathIsObstructed(destination, nearestNeighbor):
                print("Path is obstructed....")
                current = [random.randint(0, self.cellCount-1), random.randint(0, self.cellCount-1)]
                nearestNeighbor = self.getNearestNeighbour(current)
                continue
            else:
                print(f"Path is not obstructed....\nNearest Neighbour node: {self.map[nearestNeighbor[0]][nearestNeighbor[1]]}")
                
                if hasattr(self.map[nearestNeighbor[0]][nearestNeighbor[1]], 'children'):
                    self.map[nearestNeighbor[0]][nearestNeighbor[1]].children.append(destination)
                else:
                    self.map[nearestNeighbor[0]][nearestNeighbor[1]].children = [destination]

                self.map[destination[0]][destination[1]].parent = nearestNeighbor
                self.map[destination[0]][destination[1]].status = "visited"
                self.open.append(self.map[destination[0]][destination[1]])

                print(f"Distance between destination and end: {self.distance(destination, self.goal)}")
                if self.distance(destination, self.goal) < self.limit:
                    print("Node close to goal found....")
                    self.map[destination[0]][destination[1]].children.append(self.goal)
                    self.map[self.goal[0]][self.goal[1]].parent = destination
                    break

                current = [random.randint(0, self.cellCount-1), random.randint(0, self.cellCount-1)]
                nearestNeighbor = self.getNearestNeighbour(current)

            sleep(1)

        else:
            print("Path not found ")
        self.recountPath()

        return self.path, self.map
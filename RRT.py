from math import inf, sqrt
import pygame
import random
import time

# ############ pygame variables ################
pygame.init()
windowHeight, windowWidth = 600, 600
surface = pygame.display.set_mode((windowHeight, windowWidth))
running = True

# ############ UI variables ####################
wall = []
safetyWalls = []
startPoint = [400, 100]
endPoint = [200, 450]
startNode, endNode = None, None
wallThickness = 10
nodeRadius = 8
isPaused = False
colors = {"black": (0, 0, 0), "white": (255, 255, 255), "grey_black": (79, 79, 79), "red": (255, 0, 0), "green": (0, 255, 0), "orange": (255, 168, 46), "purple": (169, 103, 235), "pink": (255, 79, 158), "grey": (158, 158, 158), "light_grey": (227, 227, 227), "yellow": (255, 238, 0)}

# ############ Algorithm variables ##############
openList = []

class Node:
    def __init__(self, coordinates, parent=None, children=[]):
        self.coordinates = coordinates
        self.parent = parent
        self.children = children
    
    def __str__(self):
        return f"Node: ({self.coordinates[0]}, {self.coordinates[1]}), Parent: {self.parent}, Children: {self.children}"


def createUIWalls():
    # Horizontal walls
    for x in range(windowWidth):
        for y in range(wallThickness):
            wall.append([x, y])
            wall.append([windowHeight-x, windowWidth-y])
    
    # Verticle walls
    for x in range(wallThickness):
        for y in range(windowHeight):
            wall.append([x, y])
            wall.append([windowHeight-x, windowWidth-y])

    # Middle horizontal
    for x in range(450):
        for y in range(260, 260 + wallThickness):
            wall.append([x, y])
    
    # Top vertical wall
    for x in range(220, 220 + wallThickness):
        for y in range(150):
            wall.append([x, y])
    
    # Bottom vertical wall
    for x in range(380, 380 + wallThickness):
        for y in range(windowHeight - 240, windowHeight):
            wall.append([x, y])


def distance(point1, point2):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def getLineParameters(point1, point2):
    if abs(point1[0] - point2[0]) < 8:
        slope = float('inf')
        intercept = -1 * point1[0]
        return [slope, intercept]
    else:
        slope = (point1[1] - point2[1]) / (point1[0] - point2[0])
        intercept = point1[1] - slope*point1[0]
        return [slope, intercept]


def pathIsObstructed(destinationPoint, neighbour):
    # print(f"Checking if path between destination: {destinationPoint} and neighbour: {neighbour}")
    lineParameters = getLineParameters(destinationPoint, neighbour)

    if lineParameters[0] == float('inf'):
        print("checking for slat lines")
        for y in range(min(int(destinationPoint[1]), neighbour[1])-nodeRadius, max(int(destinationPoint[1]), neighbour[1])+nodeRadius):
            if [neighbour[0], y] in wall: # or [neighbour[0]-nodeRadius//2,  y] in wall or [neighbour[0]+nodeRadius//2,  y] in wall or [neighbour[0],  y-nodeRadius//2] in wall or [neighbour[0],  y+nodeRadius//2] in wall:
                return True
    else:
        print("checking for a straight line")
        for x in range(min(int(destinationPoint[0]), neighbour[0])-nodeRadius, max(int(destinationPoint[0]), neighbour[0])+nodeRadius):
            new_y = lineParameters[0] * x + lineParameters[1]
            if [x, int(new_y)] in wall or [x-nodeRadius//2,  int(new_y)] in wall or [x+nodeRadius//2,  int(new_y)] in wall or [x,  int(new_y)-nodeRadius//2] in wall or [x,  int(new_y)+nodeRadius//2] in wall:
                return True
    
    return False


def getDestinationPoint(currentPoint, neighbour, limit):
    if distance(currentPoint, neighbour) < limit:
        return currentPoint
    else:
        lineParameters = getLineParameters(currentPoint, neighbour)
        if lineParameters[0] == float('inf'):
            new_x = neighbour[0]
            new_y = neighbour[1] + limit
        else:
            new_x = neighbour[0] - (limit * (neighbour[0]-currentPoint[0])/distance(currentPoint, neighbour))
            new_y = lineParameters[0] * new_x + lineParameters[1]

        return [int(new_x), int(new_y)]


def getNearestNeighbour(currentPoint):
    nearestNeighbour = openList[0]

    for node in openList:
        if distance(currentPoint, node.coordinates) < distance(currentPoint, nearestNeighbour.coordinates):
            nearestNeighbour = node

    return nearestNeighbour


def solve_RRT():

    global isPaused

    upperLimit, lowerLimit = 80, 30
    currentPoint = [random.randint(0, windowWidth), random.randint(0, windowHeight)]
    nearestNeighbour = getNearestNeighbour(currentPoint)

    for i in range(5):
        print(f"Current point: {currentPoint}, Neighbour: {nearestNeighbour.coordinates}")
        pygame.draw.circle(surface, colors["pink"], currentPoint, nodeRadius, 0)

        if distance(currentPoint, nearestNeighbour.coordinates) < lowerLimit:
            pygame.draw.line(surface, colors["grey"], currentPoint, nearestNeighbour.coordinates, 2)
                    
            currentPoint = [random.randint(0, windowWidth), random.randint(0, windowHeight)]
            nearestNeighbour = getNearestNeighbour(currentPoint)
            print("New current point found")
            continue

        destinationPoint = getDestinationPoint(currentPoint, nearestNeighbour.coordinates, upperLimit)
        pygame.draw.circle(surface, colors["orange"], destinationPoint, nodeRadius, 0)
        print(f"Destination: {destinationPoint}")

        if pathIsObstructed(destinationPoint, nearestNeighbour.coordinates):
            print("Path is obstructed")
            pygame.draw.line(surface, colors["grey"], currentPoint, destinationPoint, 2)
            pygame.draw.line(surface, colors["grey"], currentPoint, nearestNeighbour.coordinates, 2)
            
            currentPoint = [random.randint(0, windowWidth), random.randint(0, windowHeight)]
            nearestNeighbour = getNearestNeighbour(currentPoint)
            print("New current point found")
            continue
        else:
            print("Path is not obstructed")
            pygame.draw.line(surface, colors["orange"], currentPoint, destinationPoint, 2)
            pygame.draw.line(surface, colors["orange"], currentPoint, nearestNeighbour.coordinates, 2)

            destinationNode, nearestNeighbourNode = None, None
            # Check if the destination and and nearestNeighbour node are present and if not then creating one
            for node in openList:
                if node.coordinates == destinationPoint:
                    destinationNode = node
                elif node.coordinates == nearestNeighbour:
                    nearestNeighbour = node
            
            if destinationNode is None:
                destinationNode = Node(destinationPoint)
                openList.append(destinationNode)    
            if nearestNeighbourNode is None:
                nearestNeighbourNode = Node(nearestNeighbour)
                openList.append(nearestNeighbour)
            
            nearestNeighbourNode.children.append(destinationNode)
            destinationNode.parent = nearestNeighbour

            print(destinationNode.coordinates, type(destinationNode.coordinates), endNode.coordinates, type(endNode.coordinates))
            if distance(destinationNode.coordinates, endNode.coordinates) < upperLimit:
                isPaused = True
                print(destinationNode.coordinates, type(destinationNode.coordinates), endNode.coordinates, type(endNode.coordinates), distance(destinationNode.coordinates, endNode.coordinates))
                    # print("Node nearest end found: " + str(destinationNode.coordinates))
                endNode.parent = destinationNode
                destinationNode.children.append(endNode)
                return

        currentPoint = [random.randint(0, windowWidth), random.randint(0, windowHeight)]
        nearestNeighbour = getNearestNeighbour(currentPoint)


if __name__ == "__main__":

    startNode, endNode = Node(startPoint), Node(endPoint)
    openList.append(startNode)

    createUIWalls()

    time.sleep(5)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        surface.fill(colors["white"])
        
        # Drawing walls
        for obstacle in wall:
            surface.set_at(tuple(obstacle), colors["grey_black"])  

        # Drawing start and end points
        pygame.draw.rect(surface, colors["green"], pygame.Rect(startPoint[0]-8, startPoint[1]-8, 16, 16))
        pygame.draw.rect(surface, colors["red"], pygame.Rect(endPoint[0]-8, endPoint[1]-8, 16, 16))
        
        solve_RRT()

        # Drawing open
        for node in openList:
            pygame.draw.circle(surface, colors["purple"], node.coordinates, nodeRadius, 0)
            if node.parent is not None:
                pygame.draw.line(surface, colors["purple"], node.coordinates, node.parent.coordinates, 2)

        if endNode.parent is None:
            pygame.display.flip()
        else:
            print("Paused......")
            running = False
            while node.parent is not None:
                print(node.coordinates)
                pygame.draw.circle(surface, colors["yellow"], node.coordinates, nodeRadius, 0)
                pygame.draw.line(surface, colors["yellow"], node.coordinates, node.parent.coordinates, 2)
                node = node.parent
            pygame.display.flip()
           
        time.sleep(1)
    else:
        print("Outside while loop........")
        surface.fill(colors["white"])

        # Drawing safety walls
        # for obstacle in safetyWalls:
        #     surface.set_at(tuple(obstacle), colors["light_grey"])
            
        # Drawing walls
        for obstacle in wall:
            surface.set_at(tuple(obstacle), colors["grey_black"])  

        # Drawing start and end points
        pygame.draw.rect(surface, colors["green"], pygame.Rect(startPoint[0]-8, startPoint[1]-8, 16, 16))
        pygame.draw.rect(surface, colors["red"], pygame.Rect(endPoint[0]-8, endPoint[1]-8, 16, 16))
        
        # Drawing open
        for node in openList:
            pygame.draw.circle(surface, colors["purple"], node.coordinates, nodeRadius, 0)
            if node.parent is not None:
                pygame.draw.line(surface, colors["purple"], node.coordinates, node.parent.coordinates, 2)

        if isPaused:
            node = endNode
            print("Paused......")
            pygame.draw.circle(surface, colors["yellow"], startNode.coordinates, nodeRadius, 0)
            pygame.draw.circle(surface, colors["yellow"], endNode.coordinates, nodeRadius, 0)
            while node.parent is not None:
                print(node.coordinates)
                pygame.draw.circle(surface, colors["yellow"], node.coordinates, nodeRadius, 0)
                pygame.draw.line(surface, colors["yellow"], node.coordinates, node.parent.coordinates, 2)
                node = node.parent
        
        pygame.display.flip()

        time.sleep(30)
from importlib.resources import path
import pygame
import time

############################# Variables ############################33
blockSize = 10
map = []
colors = {"black": (0, 0, 0), "white": (255, 255, 255), "grey_black": (79, 79, 79), "red": (255, 0, 0), "green": (0, 255, 0), "orange": (255, 168, 46), "purple": (169, 103, 235), "pink": (255, 79, 158), "grey": (158, 158, 158), "light_grey": (173, 173, 173), "yellow": (255, 238, 0)}
noOfCells = 20

running = True
#################################################################################################################################

class Node:
    # Grid status:
    # 0 -> Unoccupied
    # 1 -> Blocked
    # 2 -> Path
    # 3 -> Start point
    # 4 -> End Point
    # 5 -> Visited
    def __init__(self, x, y, status=0) -> None:
        self.x = x
        self.y = y
        self.status = status
    

    def __str__(self) -> str:
        return (f"Node ({self.x}, {self.y}): status-{self.status}")
    

def drawGrid(surface):

    global map
    surface.fill(colors["white"])
    
    for x in range(0, int(noOfCells*blockSize), blockSize):
        for y in range(0, int(noOfCells*blockSize), blockSize):
            nodeSize = 0
            # print(f"Length: {len(map)}, {len(map[0])}, {map[x//blockSize][y//blockSize]}")
            if map[x//blockSize][y//blockSize].status == 1:  # obstacle
                nodeColor = colors["black"]
            elif map[x//blockSize][y//blockSize].status == 5:  # visited
                nodeColor = colors["yellow"]
                # nodeSize = 0
            elif map[x//blockSize][y//blockSize].status == 2:   # path
                nodeColor = colors["orange"]
                # nodeSize = 0
            else:
                nodeColor = colors["light_grey"]
                nodeSize = 2
            pygame.draw.rect(surface,  nodeColor, pygame.Rect(x, y, blockSize, blockSize), nodeSize)


def initialize_grid():
    pygame.init()
    surface = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("GRID")
    surface.fill((255, 255, 0))
    return surface


def setPath(path, map):
    for x, y in path:
        map[x][y].status = 2
    
    return map


def initialiseMap(map):
    obstacles = [[x, y] for x in range(4,7) for y in range(2, 5)] + [[x, y] for x in range(13,16) for y in range(2, 5)] + [[x, y] for x in range(4, 7) for y in range(8, 11)] + [[x, y] for x in range(4, 7) for y in range(8, 11)] + [[x, y] for x in range(13,16) for y in range(8, 11)] + [[x, y] for x in range(4, 7) for y in range(14, 17)] + [[x, y] for x in range(13, 16) for y in range(14, 17)]
    # [[x, y] for x in range(8,16) for y in range(5, 13)] + [[x, y] for x in range(32, 40) for y in range(5, 13)] + [[x, y] for x in range(8,16) for y in range(20, 28)] + [[x, y] for x in range(32,40) for y in range(20, 28)] + [[x, y] for x in range(8,16) for y in range(37, 45)] + [[x, y] for x in range(32,40) for y in range(37, 45)]
    
    for o in obstacles:
        map[o[0]][o[1]].status = 1
    
    return map


def main():
    global map, running, blockSize
    
    map = [[Node(x, y) for y in range(noOfCells)] for x in range(noOfCells)]
    surface = initialize_grid()
    blockSize = 600 // noOfCells

    path = [[3, 5], [4, 5], [5, 5], [6, 5], [6, 6], [7, 6], [8, 6], [9, 6], [9, 7], [9, 8], [9, 9], [9, 10], [10, 10], [11, 10], [12, 10], [12, 11], [13, 11], [14, 11], [15, 11], [15, 12], [16, 12], [17, 12], [17, 13], [17, 14], [17, 15], [18, 15]]
    # [[4, 14], [5, 8], [6, 2], [7, 2], [8, 2], [9, 2], [10, 2], [11, 2], [12, 3], [13, 3], [14, 4], [15, 4], [16, 5], [17, 5], [18, 6], [19, 6], [20, 7], [21, 7], [22, 8], [23, 8], [24, 9], [25, 9], [26, 10], [27, 13], [28, 16], [29, 19], [30, 22], [31, 25], [32, 28], [33, 29], [34, 30], [35, 32], [36, 33], [37, 34], [38, 35], [39, 36], [40, 37], [41, 38], [42, 39], [43, 40], [44, 41]]
    # [[3, 5], [4, 5], [5, 5], [6, 5]]

    map = initialiseMap(map)
    # drawGrid(surface)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse clicked - {event.pos[0]}, {event.pos[1]}, Node: {map[int(event.pos[0]/blockSize)][int(event.pos[1]/blockSize)]}")
                map[int(event.pos[0]/blockSize)][int(event.pos[1]/blockSize)].status = 1 if map[int(event.pos[0]/blockSize)][int(event.pos[1]/blockSize)].status != 1 else 0
        
        map = setPath(path, map)

        drawGrid(surface)

        pygame.display.update()
        time.sleep(0.2)


if __name__ == "__main__":
    main()
import pygame
import time

############################# Variables ############################33
blockSize = 10
map = []
colors = {"black": (0, 0, 0), "white": (255, 255, 255), "grey_black": (79, 79, 79), "red": (255, 0, 0), "green": (0, 255, 0), "orange": (255, 168, 46), "purple": (169, 103, 235), "pink": (255, 79, 158), "grey": (158, 158, 158), "light_grey": (173, 173, 173), "yellow": (255, 238, 0)}
noOfCells = 75

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
            if map[x//blockSize][y//blockSize].status == 1:
                nodeColor = colors["black"]
            # elif map[x//blockSize][y//blockSize].status== 3:
            #     nodeColor = colors["red"]
            #     nodeSize = 0
            # elif map[x//blockSize][y//blockSize].status == 4:
            #     nodeColor = colors["green"]
            #     nodeSize = 0
            elif map[x//blockSize][y//blockSize].status == 5:
                nodeColor = colors["yellow"]
                # nodeSize = 0
            elif map[x//blockSize][y//blockSize].status == 2:
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


def main():
    global map, running, blockSize
    
    map = [[Node(x, y) for y in range(noOfCells)] for x in range(noOfCells)]
    surface = initialize_grid()
    blockSize = 600 // noOfCells
    # drawGrid(surface)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse clicked - {event.pos[0]}, {event.pos[1]}, Node: {map[int(event.pos[0]/blockSize)][int(event.pos[1]/blockSize)]}")
                map[int(event.pos[0]/blockSize)][int(event.pos[1]/blockSize)].status = 1 if map[int(event.pos[0]/blockSize)][int(event.pos[1]/blockSize)].status != 1 else 0
        
        drawGrid(surface)

        pygame.display.update()
        time.sleep(0.2)


if __name__ == "__main__":
    main()
import re
from time import sleep
import pygame

class Visualizer:
    def __init__(self, map, blockSize = 10, title = "GRID") -> None:
        ''' Initialises all the necessary variables required for the pygame console
            @param: map (List<lists>) - A list of lists containing the Node objects of a map
            @param: blockSize(int) - the size each block would occupy in the pygame window
            @param: title(String) - title of the pygame window
        '''
        pygame.init()
        self.running = True
        self.colors = {"black": (0, 0, 0), "white": (255, 255, 255), "grey_black": (79, 79, 79), "red": (255, 0, 0), "green": (0, 255, 0), "orange": (255, 168, 46), "purple": (169, 103, 235), "pink": (255, 79, 158), "grey": (158, 158, 158), "light_grey": (173, 173, 173), "yellow": (255, 238, 0)}
        
        self.blockSize = blockSize
        self.surface = pygame.display.set_mode((600, 600))
        pygame.display.set_caption(str(title))
        self.map = map
    
    def drawMap(self):
        ''' Draws and updates the map UI
        '''
        self.surface.fill(self.colors["white"])
        
        noOfCells = len(self.map)
        
        for x in range(0, int(noOfCells*self.blockSize), self.blockSize):
            for y in range(0, int(noOfCells*self.blockSize), self.blockSize):
                nodeSize = 0
                # print(f"Length: {len(map)}, {len(map[0])}, {map[x//self.blockSize][y//self.blockSize]}")
                if self.map[x//self.blockSize][y//self.blockSize].status == "obstacle":
                    nodeColor = self.colors["black"]
                elif self.map[x//self.blockSize][y//self.blockSize].status == "start":
                    nodeColor = self.colors["green"]
                elif self.map[x//self.blockSize][y//self.blockSize].status == "goal":
                    nodeColor = self.colors["red"]
                elif self.map[x//self.blockSize][y//self.blockSize].status == "visited":
                    nodeColor = self.colors["yellow"]
                elif self.map[x//self.blockSize][y//self.blockSize].status == "path":
                    nodeColor = self.colors["orange"]
                else: # unvisited node
                    nodeColor = self.colors["light_grey"]
                    nodeSize = 2
                pygame.draw.rect(self.surface,  nodeColor, pygame.Rect(x, y, self.blockSize, self.blockSize), nodeSize)
    
    def run(self):
        ''' Displays the latest map with changes after every 0.2 secs
        '''
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse clicked - {event.pos[0]}, {event.pos[1]}, Node: {self.map[int(event.pos[0]/self.blockSize)][int(event.pos[1]/self.blockSize)]}")
                self.map[int(event.pos[0]/self.blockSize)][int(event.pos[1]/self.blockSize)].status = "obstacle" if self.map[int(event.pos[0]/self.blockSize)][int(event.pos[1]/self.blockSize)].status in ["unvisited", "path", "visited"] else "unvisited"
            

        self.drawMap()

        pygame.display.update()
        return True
        
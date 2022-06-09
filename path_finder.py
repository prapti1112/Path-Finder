import imp
from sys import path as sys_path
from os import getcwd
import node
from visualizer import Visualizer
from time import sleep

class PathFinder:
    
    def __init__(self, solver, map, cellCount = 20) -> None:
        ''' Constructor of a path finder
        @param: solver(String) - represents the path finding algorithm being used
        @param: map(List<List>) - contains the map of the environment
        @param: cellCount(int) - contains number of cells in the map
        '''

        self.solver = solver
        self.map = map
        self.path = []
        self.cellCount = cellCount
        self.running = True
    
    def updatePathStatus(self):
        for nodeY, nodeX in self.path:
            self.map[nodeX][nodeY].status = "path"
        
    def findPath(self):
        
        while self.running:
            if self.solver == 'A_star':        
                sys_path.append(getcwd() + '/algorithms/')
                import a_star
                self.solver = a_star.A_star()
            
            self.path = self.solver.getPath(self.map)
            self.updatePathStatus()
            self.running = Visualizer(self.map, 30).run()
            sleep(0.2)
          


if __name__ == "__main__":
    print("Hello there")


    map = [[node.Node(x, y) for y in range(20)] for x in range(20)]
    path_finder = PathFinder('A_star', map, 30)
    path_finder.findPath()

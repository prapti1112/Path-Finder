from sys import path as sys_path
from os import getcwd
import node
from visualizer import Visualizer
from time import sleep

class PathFinder:
    
    def __init__(self, solver, map, startCoordinate = [], goalCoordinate = [], cellCount = 20) -> None:
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
        self.start = startCoordinate
        self.goal = goalCoordinate
    
    def updatePathStatus(self):
        for node in self.path:
            self.map[node.x][node.y].status = "path"
        self.path[0].status = "start"
        self.path[-1].status = "goal"
        
    def findPath(self):
        
        while self.running:
            if self.solver == 'A_star':        
                sys_path.append(getcwd() + '/algorithms/')
                import a_star
                self.solver = a_star.A_star(startCoordinate, goalCoordinate)
            
            self.running = Visualizer(self.map, 30).run()
            
            self.path, self.map = self.solver.getPath(self.map, self.start, self.goal)
            self.updatePathStatus()
            
            sleep(0.5)
          


if __name__ == "__main__":

    map = [[node.Node(x, y) for y in range(20)] for x in range(20)]
    startCoordinate, goalCoordinate = [3, 5], [9, 9]

    map[startCoordinate[0]][startCoordinate[1]].status, map[goalCoordinate[0]][goalCoordinate[1]].status = "start", "goal"

    path_finder = PathFinder('A_star', map, startCoordinate, goalCoordinate, 30)
    path_finder.findPath()

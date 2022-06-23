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
            sys_path.append(getcwd() + '/algorithms/')
            if self.solver == 'A_star':                        
                import a_star
                self.solver = a_star.A_star(startCoordinate, goalCoordinate)
            elif self.solver == 'RRT':
                import rrt
                self.solver = rrt.RRT(startCoordinate, goalCoordinate)
            
            self.running = Visualizer(self.map, 30).run()
            
            self.path, self.map = self.solver.getPath(self.map, self.start, self.goal)
            
            if len(self.path):
                self.updatePathStatus()
            
            sleep(0.5)
          

def initialiseMap(map):
    
    obstacles = [[x, y] for x in range(4,7) for y in range(2, 5)] + [[x, y] for x in range(13,16) for y in range(2, 5)] + [[x, y] for x in range(4, 7) for y in range(8, 11)] + [[x, y] for x in range(4, 7) for y in range(8, 11)] + [[x, y] for x in range(13,16) for y in range(8, 11)] + [[x, y] for x in range(4, 7) for y in range(14, 17)] + [[x, y] for x in range(13, 16) for y in range(14, 17)]
    
    for o in obstacles:
        map[o[0]][o[1]].status = "obstacle"
    
    return map
        

if __name__ == "__main__":

    map = [[node.Node(x, y) for y in range(20)] for x in range(20)]
    startCoordinate, goalCoordinate = [3, 5], [15, 18]

    map[startCoordinate[0]][startCoordinate[1]].status, map[goalCoordinate[0]][goalCoordinate[1]].status = "start", "goal"
    map = initialiseMap(map)

    path_finder = PathFinder('RRT', map, startCoordinate, goalCoordinate, 30)
    path_finder.findPath()

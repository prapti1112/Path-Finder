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
        self.originalMap = map
        self.path = []
        self.cellCount = cellCount
        self.running = True
        self.start = startCoordinate
        self.goal = goalCoordinate
    
    def updatePathStatus(self):
        for node in self.path:
            self.map[node.x][node.y].status = "path"
        self.map[self.start[0]][self.start[1]].status, self.map[self.goal[0]][self.goal[1]].status  = "start", "goal"
    
    def resetMap(self):
        self.map = [[node.Node(x, y) for y in range(self.cellCount)] for x in range(self.cellCount)]
        # obstacles = [[x, y] for x in range(8,16) for y in range(5, 13)] + [[x, y] for x in range(32, 40) for y in range(5, 13)] + [[x, y] for x in range(8,16) for y in range(20, 28)] + [[x, y] for x in range(32,40) for y in range(20, 28)] + [[x, y] for x in range(8,16) for y in range(37, 45)] + [[x, y] for x in range(32,40) for y in range(37, 45)]
        obstacles = [[x, y] for x in range(4,7) for y in range(2, 5)] + [[x, y] for x in range(13,16) for y in range(2, 5)] + [[x, y] for x in range(4, 7) for y in range(8, 11)] + [[x, y] for x in range(4, 7) for y in range(8, 11)] + [[x, y] for x in range(13,16) for y in range(8, 11)] + [[x, y] for x in range(4, 7) for y in range(14, 17)] + [[x, y] for x in range(13, 16) for y in range(14, 17)]

        for o in obstacles:
            self.map[o[0]][o[1]].status = "obstacle"

        self.map[self.start[0]][self.start[1]].status = "start"
        self.map[self.goal[0]][self.goal[1]].status = "goal"


    def findPath(self):
        
        while self.running:
            sys_path.append(getcwd() + '/algorithms/')
            if self.solver == 'A_star':                        
                import a_star
                self.solver = a_star.A_star(startCoordinate, goalCoordinate)
            elif self.solver == 'RRT':
                import rrt
                self.solver = rrt.RRT(startCoordinate, goalCoordinate, cellCount = self.cellCount)
            elif self.solver == "Q_Learning":
                import q_learning
                self.solver = q_learning.Q_Learning(goal=[self.goal[1], self.goal[0]], start=self.start, map=self.map, noOfActions=4, noOfCells=self.cellCount)
            
            visualizer = Visualizer(self.cellCount)
            print("First showing....")
            self.running = visualizer.run(self.map)
            sleep(5)

            self.resetMap()

            print("Second showing....")
            self.running = visualizer.run(self.map)            
            sleep(0.2)

            self.path, self.map = self.solver.getPath(self.map, self.start, self.goal)
            
            if len(self.path):
                self.updatePathStatus()
            
            # sleep(5)
          

def initialiseMap(map):
    
    obstacles = [[x, y] for x in range(4,7) for y in range(2, 5)] + [[x, y] for x in range(13,16) for y in range(2, 5)] + [[x, y] for x in range(4, 7) for y in range(8, 11)] + [[x, y] for x in range(4, 7) for y in range(8, 11)] + [[x, y] for x in range(13,16) for y in range(8, 11)] + [[x, y] for x in range(4, 7) for y in range(14, 17)] + [[x, y] for x in range(13, 16) for y in range(14, 17)]
    
    # 1. (8, 5) ---> (15, 12)
    # 2. (32, 5) ---> (39, 12)
    # 3. (8, 20) ---> (15, 27)
    # 4. (32, 20) ---> (39, 27)
    # 5. (8, 37) ---> (15, 44)
    # 6. (32, 37) ---> (39, 44)
    # obstacles = [[x, y] for x in range(8,16) for y in range(5, 13)] + [[x, y] for x in range(32, 40) for y in range(5, 13)] + [[x, y] for x in range(8,16) for y in range(20, 28)] + [[x, y] for x in range(32,40) for y in range(20, 28)] + [[x, y] for x in range(8,16) for y in range(37, 45)] + [[x, y] for x in range(32,40) for y in range(37, 45)]
    
    for o in obstacles:
        map[o[0]][o[1]].status = "obstacle"
    
    return map
        

if __name__ == "__main__":

    noOfCells = 20

    map = [[node.Node(x, y) for y in range(noOfCells)] for x in range(noOfCells)]
    startCoordinate, goalCoordinate = [3, 5], [15, 18]
    # startCoordinate, goalCoordinate = [4, 14], [44, 41]

    map[startCoordinate[0]][startCoordinate[1]].status, map[goalCoordinate[0]][goalCoordinate[1]].status = "start", "goal"
    map = initialiseMap(map)

    path_finder = PathFinder('Q_Learning', map, startCoordinate, goalCoordinate, noOfCells)
    path_finder.findPath()

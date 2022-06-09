# import node

class A_star:
    def __init__(self) -> None:
        print("Hello there from A* solver")
    
    def getPath(self, map):
        return [[i, i] for i in range(2, 6) if map[i][i].status != "obstacle"]
class Node:
    def __init__(self, x, y, status="unvisited") -> None:
        self.x = x
        self.y = y
        self.status = status
    
    def __str__(self) -> str:
        return f"Node ({self.x}, {self.y}): {self.status}"
    

    def __eq__(self, __o) -> bool:
        # print(f"Nodes being compared: {self}, {__o}")

        return (self.x == __o.x) and (self.y == __o.y)
class Node:
    def __init__(self, x, y, status="unvisited") -> None:
        self.x = x
        self.y = y
        self.status = status
    
    def __str__(self) -> str:
        return f"Node ({self.x}, {self.y}): {self.status}"
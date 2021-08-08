# Path-Finder
This repository consists of implementations of different path finding algorithms in python using pygame
<br><br>

## Requirement:
<ul>
<li> python 3.x </li>
<li> pygame </li>
</ul>
<br>

## Algorithms used:

### Rapidly exploring random trees
``` diff
1. Select a random point 

2. Find the nearest neighbour of the point selected point random point 

3. for i: 0 -> n (n -> number of points to be randomely chossen in one pass)
    if distance between randomly chosen point is more than the preset step size find a distination point
    check if path between destination point and nearest neighbour is obstructed
      yes -> choose a new point randomly
                continue to next pass
      no  -> add the destination node as child of the nearest neighbour
              add the nearestNeighbour node as a parent of the destination node
              if nearestNeighbout node is not already present in the openList then append the node
              if destination node is not already present in the openList then append the node
              if the distance between destination node and end node is less than the limit
                   connect destination node and end node and return to main
    Select a new random point 
    Find the nearest neighbour of the point selected point random point 
```
<br>

## Implementation demos:

### Rapidly exploring random trees
![RRT demo](https://github.com/prapti1112/Path-Finder/blob/python/videos/RRT%20implementaion.gif)

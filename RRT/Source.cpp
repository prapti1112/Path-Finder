#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include <iostream>
using namespace std;
#include "olcConsoleGameEngine.h"

class PathFinder_RRT : public olcConsoleGameEngine {
public:
	PathFinder_RRT() {
		m_sAppName = L"RRT Path Finding";
	}

	struct Node
	{
		int x;
		int y;
		bool isObstacle;
		bool isRandomSelectedNode;
		bool isVisited;
		Node* parent;
		vector<Node*> children;
	};

	Node* nodes = nullptr;

	int mapWidth = 50;
	int mapHeight = 50;

	vector<pair<int, int>> wall;
	vector<Node*> openList;

	Node* nodeStart = nullptr;
	Node* nodeEnd = nullptr;

	virtual bool OnUserCreate() {
		nodes = new Node[mapWidth * mapHeight];

		// map walls formation
		wall.push_back(make_pair(0, 0));
		for (int i = 1; i < mapWidth; i++) {
			wall.push_back(make_pair(0, i));
			wall.push_back(make_pair(i, 0));
			wall.push_back(make_pair(mapWidth - 1, i));
			wall.push_back(make_pair(i, mapHeight - 1));
		}

		for (int i = 0; i < 6; i++)
			wall.push_back(make_pair(6, i));
		for (int i = 0; i < mapWidth - 5; i++)
			wall.push_back(make_pair(i, 9));
		for (int i = 1; i < 6; i++)
			wall.push_back(make_pair(12, mapHeight - i));

		for (int x = 0; x < mapWidth; x++)
			for (int y = 0; y < mapHeight; y++) {
				nodes[y * mapWidth + x].x = x;
				nodes[y * mapWidth + x].y = y;
				nodes[y * mapWidth + x].parent = nullptr;
				nodes[y * mapWidth + x].isRandomSelectedNode = false;
				nodes[y * mapWidth + x].isVisited = false;

				if (find(wall.begin(), wall.end(), make_pair(x, y)) != wall.end())
					nodes[y * mapWidth + x].isObstacle = true;
				else
					nodes[y * mapWidth + x].isObstacle = false;
			}

		nodeStart = &nodes[5 * mapWidth + (mapWidth - 8)];
		nodeEnd = &nodes[(mapHeight - 5) * mapWidth + 7];

		return true;
	}


	// Helper functions for the Algorithm
	bool isPathObstructed(Node* n1, Node* n2) {
		pair<float, float> line_params = getLineParameters(n1, n2);
		int new_y;
		for (int i = min(n1->x, n2->x); i <= max(n1->x, n2->x); i++) {
			if (line_params.first != INFINITY)
				new_y = i * line_params.first + line_params.second;
			else
				new_y = min(n1->y, n2->y) + 1;
			if (nodes[new_y * mapWidth + i].isObstacle)
				return true;
		}

		return false;
	}

	pair<float, float> getLineParameters(Node* n1, Node* n2) {
		float slope, intercept;

		if (n1->x == n2->x) {
			slope = INFINITY;
			intercept = n1->x;
		}
		else {
			slope = float(n1->y - n2->y) / (n1->x - n2->x);
			intercept = n1->y - slope * n1->x;
		}

		return make_pair(slope, intercept);
	}

	float distance(Node* a, Node* b) {
		return sqrtf((a->x - b->x) * (a->x - b->x) + (a->y - b->y) * (a->y - b->y));
	}


	Node* getTravelDestination(Node* currentNode, Node* neighbour, int limit) {
		if (distance(currentNode, neighbour) <= limit)
			return currentNode;
		else {
			pair<float, float> line_params = getLineParameters(currentNode, neighbour);
			int newNode_y, newNode_x;
			if (line_params.first != INFINITY) {
				newNode_x = neighbour->x - ((limit * float(neighbour->x - currentNode->x) / distance(currentNode, neighbour)));
				newNode_y = line_params.first * newNode_x + line_params.second;
			}
			else {
				newNode_y = neighbour->y + limit;
				newNode_x = neighbour->x;
			}

			return &nodes[newNode_y * mapWidth + newNode_x];
		}
	}

	Node* getNearestNeighbour(Node* currentNode) {

		// Naive approach
		Node* nearestNeighbour = openList.at(0);
		for (auto node : openList) {
			if (distance(currentNode, node) < distance(currentNode, nearestNeighbour))
				nearestNeighbour = node;
		}
		return nearestNeighbour;
	}

	// Implementation start for the algorithm
	bool solve_RRT() {

		int limit = 3;

		Node* nearestNeighbour = nodeStart;
		Node* currentNode = &nodes[(rand() % mapHeight) * mapWidth + (rand() % mapWidth)];
		Node* destinationNode;
		openList.push_back(nodeStart);

		while (currentNode != nodeEnd) {
			currentNode->isRandomSelectedNode = true;

			destinationNode = getTravelDestination(currentNode, nearestNeighbour, limit);

			destinationNode->isVisited = true;

			if (isPathObstructed(destinationNode, nearestNeighbour)) {
				currentNode->isRandomSelectedNode = false;
				currentNode = &nodes[(rand() % mapHeight) * mapWidth + (rand() % mapWidth)];
				nearestNeighbour = getNearestNeighbour(currentNode);
				continue;
			}
			else {
				nearestNeighbour->children.push_back(destinationNode);
				destinationNode->parent = nearestNeighbour;
				destinationNode->isVisited = true;
				openList.push_back(destinationNode);

				if (distance(destinationNode, nodeEnd) <= limit) {
					destinationNode->children.push_back(nodeEnd);
					nodeEnd->parent = destinationNode;
					break;
				}
			}

			currentNode->isRandomSelectedNode = false;

			currentNode = &nodes[(rand() % mapHeight) * mapWidth + (rand() % mapWidth)];
			while (find(openList.begin(), openList.end(), currentNode) != openList.end())
				currentNode = &nodes[(rand() % mapHeight) * mapWidth + (rand() % mapWidth)];
			nearestNeighbour = getNearestNeighbour(currentNode);
		}

		return true;
	}

	virtual bool OnUserUpdate(float fElapsedTime) {

		int nodeSize = 8;
		int nodeBorder = 1;

		// clearing the screen
		Fill(0, 0, ScreenWidth(), ScreenHeight(), L' ');

		int selectedNodeX = m_mousePosX / nodeSize;
		int selectedNodeY = m_mousePosY / nodeSize;

		if (m_mouse[0].bReleased) {
			if (selectedNodeX >= 0 && selectedNodeX < mapWidth)
				if (selectedNodeY >= 0 && selectedNodeY < mapHeight)
				{
					if (m_keys[VK_SHIFT].bHeld)
						nodeStart = &nodes[selectedNodeY * mapWidth + selectedNodeX];
					else if (m_keys[VK_CONTROL].bHeld)
						nodeEnd = &nodes[selectedNodeY * mapWidth + selectedNodeX];
					else
						nodes[selectedNodeY * mapWidth + selectedNodeX].isObstacle = !nodes[selectedNodeY * mapWidth + selectedNodeX].isObstacle;

				}
		}

		// drawing the nodes
		for (int x = 0; x < mapWidth; x++)
			for (int y = 0; y < mapHeight; y++)
			{
				Fill(x * nodeSize + nodeBorder, y * nodeSize + nodeBorder,
					(x + 1) * nodeSize - nodeBorder, (y + 1) * nodeSize - nodeBorder,
					nodes[y * mapWidth + x].isObstacle || nodes[y * mapWidth + x].isVisited || nodes[y * mapWidth + x].isRandomSelectedNode ? PIXEL_SOLID : PIXEL_HALF, nodes[y * mapWidth + x].isObstacle ? FG_WHITE : (nodes[y * mapWidth + x].isRandomSelectedNode) ? FG_DARK_YELLOW : (nodes[y * mapWidth + x].isVisited) ? FG_MAGENTA : FG_BLUE);

				if (&nodes[y * mapWidth + x] == nodeStart)
					Fill(x * nodeSize + nodeBorder, y * nodeSize + nodeBorder, (x + 1) * nodeSize - nodeBorder, (y + 1) * nodeSize - nodeBorder, PIXEL_SOLID, FG_GREEN);

				if (&nodes[y * mapWidth + x] == nodeEnd)
					Fill(x * nodeSize + nodeBorder, y * nodeSize + nodeBorder, (x + 1) * nodeSize - nodeBorder, (y + 1) * nodeSize - nodeBorder, PIXEL_SOLID, FG_RED);

				solve_RRT();
			}


		// drawing the final path
		if (nodeEnd != nullptr)	{
			Node* p = nodeEnd;
			while (p->parent != nullptr)
			{
				DrawLine(p->x * nodeSize + nodeSize / 2, p->y * nodeSize + nodeSize / 2,
					p->parent->x * nodeSize + nodeSize / 2, p->parent->y * nodeSize + nodeSize / 2, PIXEL_SOLID, FG_YELLOW);

				p = p->parent;
			}
		}
		return true;
	}
};

int main() {
	PathFinder_RRT rrt;
	rrt.ConstructConsole(150, 150, 2, 2);
	rrt.Start();
	return 0;
}
#!/usr/bin/python3


from CS312Graph import *
import time
import math


class NetworkRoutingSolver:
    def __init__(self):
        self.dist = None
        self.prev = None

    def initializeNetwork(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        currIndex = self.dest

        while currIndex != self.source:
            prevNode = self.network.nodes[self.prev[currIndex]]
            neighbors = prevNode.neighbors
            selectedEdge = None
            for neighbor in neighbors:
                if neighbor.dest.node_id == currIndex:
                    selectedEdge = neighbor

            if not (selectedEdge is None):
                path_edges.insert(0, (selectedEdge.src.loc, selectedEdge.dest.loc, '{:.0f}'.format(selectedEdge.length)))
                total_length += selectedEdge.length
            else:
                print("Something is wrong, line 33")

            currIndex = prevNode.node_id



            # find the edge in the prevNode neighbors that connects to current node



        #  start at the end node, take the edge to the previous
        #  add the distance to the total, then go to the next previous
        #  once you get to the start node you are done

        # edges_left = 3
        # while edges_left > 0:
        #     edge = node.neighbors[2]
        #     path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
        #     total_length += edge.length
        #     node = edge.dest
        #     edges_left -= 1
        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        self.dist, self.prev = self.dijkstra(self.source)
        t2 = time.time()
        return t2 - t1

    def dijkstra(self, startNode):
        numNodes = len(self.network.nodes)
        dist = [math.inf for _ in range(numNodes)]
        prev = [None for _ in range(numNodes)]

        dist[startNode] = 0
        priorityQueue = ArrayQueue(self.network.nodes)
        while numNodes > 0:
            currNode = priorityQueue.deletemin(dist)
            numNodes -= 1
            neighbors = self.network.nodes[currNode].neighbors
            for neighbor in neighbors:
                neighborID = neighbor.dest.node_id
                if dist[neighborID] > (dist[currNode] + neighbor.length):
                    dist[neighborID] = dist[currNode] + neighbor.length
                    prev[neighborID] = currNode
                    priorityQueue.decreasekey()

        return dist, prev

class Queue:
    def insert(self, node):
        pass

    def deletemin(self, dist):
        pass

    def decreasekey(self):
        pass

    def isEmpty(self):
        pass


class ArrayQueue(Queue):
    def __init__(self, nodes):
        #  Queue.__init__(self, nodes)
        #  makeQueue
        self.priorityQueue = []
        for node in nodes:
            self.insert(node.node_id)

    def insert(self, node):
        #  Do we even need this for the array?
        self.priorityQueue.append(node)
        pass

    def deletemin(self, dist):
        #  you cant start at 0 every time because if dist[0] is the smallest length it will get stuck
        minIndex = 0
        while self.priorityQueue[minIndex] < 0:
            minIndex += 1

        for node in self.priorityQueue:
            if node >= 0:
                if dist[node] < dist[minIndex] and self.priorityQueue[node] >= 0:
                    minIndex = node

        print("minIndex: " + str(minIndex))
        self.priorityQueue[minIndex] = -1
        return minIndex

    def decreasekey(self):
        pass

    def isEmpty(self):
        for index in self.priorityQueue:
            if index >= 0:
                return False

        return True

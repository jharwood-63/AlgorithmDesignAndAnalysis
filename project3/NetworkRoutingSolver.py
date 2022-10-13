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

        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        self.dist, self.prev = self.dijkstra(self.source, use_heap)
        t2 = time.time()
        return t2 - t1

    def dijkstra(self, startNode, use_heap):
        numNodes = len(self.network.nodes)
        dist = [math.inf for _ in range(numNodes)]
        prev = [None for _ in range(numNodes)]

        dist[startNode] = 0
        #  priorityQueue = None
        if use_heap:
            priorityQueue = HeapQueue(self.network.nodes, dist)
        else:
            priorityQueue = ArrayQueue(self.network.nodes, dist)


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

class HeapQueue(Queue):
    def __init__(self, nodes, dist):
        self.heap = []
        self.makeQueue(nodes, dist)

    def makeQueue(self, nodes, dist):
        # put them all in an array
        for node in nodes:
            self.insert(node)

        # sort them correctly
        for i in range(len(nodes)-1, -1, -1):
            self.siftdown(self.heap[i], i, dist)

    def insert(self, node):
        self.heap.append(node.node_id)

    def deletemin(self, dist):
        return 0

    def decreasekey(self):
        return 0

    def siftdown(self, x, i, dist):
        #  this is not working
        minIndex = self.minchild(i, dist)

        while minIndex != 0 and dist[minIndex] < dist[x]:
            self.heap[i] = minIndex
            i = minIndex
            minIndex = self.minchild(i, dist)

        self.heap[i] = x

    def minchild(self, i, dist):
        if ((2*i) + 1) >= len(self.heap):
            return 0
        else:
            #  minIndex = min(dist[self.heap[(2*i)+1]], dist[self.heap[(2*i)+2]])
            if dist[self.heap[(2*i)+1]] <= dist[self.heap[(2*i)+2]]:
                return self.heap[(2*i)+1]
            else:
                return self.heap[(2*i)+2]

            #  return minIndex
            # return min(dist[j] for j in range((2*i) + 1, min(len(self.heap), (2*i) + 1)))



class ArrayQueue(Queue):
    def __init__(self, nodes, dist):
        self.priorityQueue = []
        for node in nodes:
            self.insert(node.node_id)

    def insert(self, node):
        self.priorityQueue.append(node)

    def deletemin(self, dist):
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

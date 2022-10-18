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
            prevIndex = self.prev[currIndex]
            if prevIndex is not None:
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
            else:
                total_length = math.inf
                break

        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        self.dist = []
        self.prev = []
        self.dijkstra(self.source, use_heap)
        t2 = time.time()
        return t2 - t1

    def dijkstra(self, startNode, use_heap):  # Heap: O(nlog2(n)), Array: O(n^2)
        numNodes = len(self.network.nodes)
        self.dist = [math.inf for _ in range(numNodes)]  # O(n)
        self.prev = [None for _ in range(numNodes)]  # O(n)

        self.dist[startNode] = 0
        if use_heap:
            priorityQueue = HeapQueue(self.network.nodes, self.source)  # O(n)
        else:
            priorityQueue = ArrayQueue(self.network.nodes)  # O(n)

        while numNodes > 0:  # O(n)
            currNode = priorityQueue.deletemin(self.dist)  # O(log n) for heap, O(n) for array
            numNodes -= 1
            neighbors = self.network.nodes[currNode].neighbors
            for neighbor in neighbors:  # O(3)
                neighborID = neighbor.dest.node_id
                if self.dist[neighborID] > (self.dist[currNode] + neighbor.length):
                    self.dist[neighborID] = self.dist[currNode] + neighbor.length
                    self.prev[neighborID] = currNode
                    priorityQueue.decreasekey(self.dist, neighborID)  # O(log2(n)) for heap, O(1) for array

class HeapQueue:
    def __init__(self, nodes, startNode):
        self.heap = []
        self.makeQueue(nodes, startNode)

    def makeQueue(self, nodes, startNode):
        self.heap.append(startNode)
        for node in nodes:
            nodeId = node.node_id
            if nodeId != startNode:
                self.heap.append(nodeId)

    def insert(self, node):
        self.heap.append(node.node_id)

    def deletemin(self, dist):
        if len(self.heap) == 0:
            return None
        else:
            minDist = self.heap[0]
            self.siftdown(self.heap[-1], 0, dist)
            self.heap.pop()

            return minDist

    def decreasekey(self, dist, x):
        try:
            self.bubbleup(x, self.heap.index(x), dist)  # O(log2(n))
        except ValueError:
            pass

    def bubbleup(self, x, i, dist):
        p = i // 2
        while i > 0 and dist[self.heap[p]] > dist[x]:
            self.heap[i] = self.heap[p]
            i = p
            p = i // 2

        self.heap[i] = x

    def siftdown(self, x, i, dist):
        minIndex = self.minchild(i, dist)  # returns index in heap
        while minIndex >= 0 and dist[self.heap[minIndex]] < dist[x]:
            self.heap[i] = self.heap[minIndex]
            i = minIndex
            minIndex = self.minchild(i, dist)

        self.heap[i] = x

    def minchild(self, i, dist):
        firstChildIdx = (2*i)+1
        secondChildIdx = (2*i)+2
        if secondChildIdx < len(self.heap) and firstChildIdx < len(self.heap):
            if dist[self.heap[firstChildIdx]] < dist[self.heap[secondChildIdx]]:
                return firstChildIdx
            else:
                return secondChildIdx
        elif firstChildIdx < len(self.heap):
            return firstChildIdx
        else:
            return -1

class ArrayQueue:
    def __init__(self, nodes):
        self.priorityQueue = []
        for node in nodes:
            self.priorityQueue.append(node.node_id)

    def insert(self, node):
        self.priorityQueue.append(node)

    def deletemin(self, dist):
        minIndex = 0
        while self.priorityQueue[minIndex] < 0:
            minIndex += 1

        for node in self.priorityQueue:
            if dist[node] < dist[minIndex] and node >= 0:
                minIndex = node

        self.priorityQueue[minIndex] = -1
        return minIndex

    def decreasekey(self, dist, x):
        pass

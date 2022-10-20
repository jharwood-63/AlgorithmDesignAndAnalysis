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

        while currIndex != self.source:  # Worst case: O(n)
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

    def dijkstra(self, startNode, use_heap):  # Heap: O(nlog(n)), Array: O(n^2)
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
                    priorityQueue.decreasekey(self.dist, neighborID)  # O(log(n)) for heap, O(1) for array

class HeapQueue:
    def __init__(self, nodes, startNode):
        self.heap = []
        self.indices = []  # indices -> index is nodeID, value is index of heap
        self.makeQueue(nodes, startNode)

    def makeQueue(self, nodes, startNode):  # O(n)
        self.heap.append(startNode)
        index = 1
        for node in nodes:
            nodeId = node.node_id
            if nodeId != startNode:
                self.heap.append(nodeId)
                self.indices.append(index)
            else:
                self.indices.append(0)

            index += 1

    def insert(self, node, dist):  # O(log(n))
        self.heap.append(node.node_id)
        self.bubbleup(node.node_id, (len(self.heap) - 1), dist)

    def deletemin(self, dist):  # O(log(n))
        if len(self.heap) == 0:
            return None
        else:
            minDist = self.heap[0]
            if len(self.heap) > 1:
                self.heap[0] = self.heap[-1]
                self.indices[self.heap[-1]] = 0
                self.heap.pop()
                self.indices[minDist] = len(self.heap)
                self.siftdown(self.heap[0], 0, dist)

            return minDist

    def decreasekey(self, dist, x):  # O(log(n))
        index = self.indices[x]
        if index < len(self.heap):
            self.bubbleup(x, index, dist)  # O(log(n))

    def bubbleup(self, x, i, dist):
        p = i // 2
        while i > 0 and dist[self.heap[p]] > dist[x]:
            self.heap[i] = self.heap[p]
            self.heap[p] = x

            temp = self.indices[self.heap[i]]
            self.indices[self.heap[i]] = self.indices[self.heap[p]]
            self.indices[self.heap[p]] = temp

            i = p
            p = i // 2

    def siftdown(self, x, i, dist):  # O(log(n))
        minIndex = self.minchild(i, dist)  # O(1)
        while minIndex != 0 and dist[self.heap[minIndex]] < dist[x]:
            self.heap[i] = self.heap[minIndex]
            self.heap[minIndex] = x

            temp = self.indices[self.heap[i]]
            self.indices[self.heap[i]] = self.indices[self.heap[minIndex]]
            self.indices[self.heap[minIndex]] = temp

            i = minIndex
            minIndex = self.minchild(i, dist)

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

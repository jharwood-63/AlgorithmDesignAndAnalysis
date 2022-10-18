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
                # print("unreachable")
                total_length = math.inf
                break

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
        if use_heap:
            # t3 = time.time()
            priorityQueue = HeapQueue(self.network.nodes, dist)
            # t4 = time.time()
            # print("makeQueue: " + str(t4-t3))
        else:
            priorityQueue = ArrayQueue(self.network.nodes)

        while numNodes > 0:
            # t5 = time.time()
            currNode = priorityQueue.deletemin(dist)
            # t6 = time.time()
            # print("deletemin: " + str(t6-t5))
            if numNodes % 1000 == 0:
                print("numNodes: " + str(numNodes))
            numNodes -= 1
            neighbors = self.network.nodes[currNode].neighbors
            for neighbor in neighbors:
                neighborID = neighbor.dest.node_id
                if dist[neighborID] > (dist[currNode] + neighbor.length):
                    dist[neighborID] = dist[currNode] + neighbor.length
                    prev[neighborID] = currNode
                    # t7 = time.time()
                    priorityQueue.decreasekey(dist, neighborID)
                    # t8 = time.time()
                    # print("decreasekey: " + str(t8-t7))

        return dist, prev

class HeapQueue:
    def __init__(self, nodes, dist):
        # self.startIndex = 0
        self.heap = []
        self.makeQueue(nodes, dist)

    def makeQueue(self, nodes, dist):
        # print("in makequeue")
        for node in nodes:
            self.heap.append(node.node_id)

        for i in range(len(nodes)-1, -1, -1):
            self.siftdown(self.heap[i], i, dist)

    def insert(self, node):
        self.heap.append(node.node_id)

    def deletemin(self, dist):
        # print("In deletemin\n")
        if len(self.heap) == 0:
            # print("The heap is empty, that's not good \n")
            return None
        else:
            # print("removing " + str(self.heap[0]) + "\n")
            minDist = self.heap[0]
            # self.startIndex += 1
            self.heap.pop(0)
            if len(self.heap) > 1:
                self.heap.insert(0, self.heap[len(self.heap) - 1])
                self.heap.pop()
                self.siftdown(self.heap[0], 0, dist)

            return minDist

    def decreasekey(self, dist, x):
        # print("In decreasekey")
        # print("x: " + str(x))
        try:
            self.bubbleup(x, self.heap.index(x), dist)
        except ValueError:
            pass
            # print("ValueError line 120")

    def bubbleup(self, x, i, dist):
        # print("In bubbleup")
        p = i // 2
        while i > 0 and dist[self.heap[p]] > dist[x]:
            self.heap[i] = self.heap[p]
            self.heap[p] = x
            i = p
            p = i // 2

    def siftdown(self, x, i, dist):
        # print("In siftdown\n")
        minIndex = self.minchild(i, dist)  # returns index in heap

        while minIndex != 0 and dist[self.heap[minIndex]] < dist[x]:
            self.heap[i] = self.heap[minIndex]
            self.heap[minIndex] = x
            i = minIndex
            minIndex = self.minchild(i, dist)

    def minchild(self, i, dist):
        firstChildIdx = (2*i)+1
        secondChildIdx = (2*i)+2
        if secondChildIdx >= len(self.heap) and firstChildIdx >= len(self.heap):
            return 0  # no children
        elif secondChildIdx >= len(self.heap):
            return firstChildIdx  # only one child
        else:  # both children
            if dist[self.heap[firstChildIdx]] <= dist[self.heap[secondChildIdx]]:
                return firstChildIdx
            else:
                return secondChildIdx

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

#!/usr/bin/python3


from CS312Graph import *
import time
import math


class NetworkRoutingSolver:
    def __init__(self):
        pass

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
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        self.dijkstra(self.source)
        t2 = time.time()
        return (t2 - t1)

    def dijkstra(self, startNode):
        #  initialize distance and previous arrays to infinity and NULL
        #  set the index of the start node in distance array to 0
        #  create the queue -> priorityQueue = Queue(self.network.nodes)
        #  loop while priority queue is not empty
        #  delete the shortest distance from the priority queue
        #  loop all neighbors of current node (returned from deletemin)

        numNodes = len(self.network.nodes)
        dist = [math.inf for i in range(numNodes)]
        prev = [None for i in range(numNodes)]

        dist[startNode] = 0
        priorityQueue = ArrayQueue(self.network.nodes)
        while not priorityQueue.isEmpty():
            currNode = priorityQueue.deletemin(dist)
            neighbors = self.network.nodes[currNode].neighbors
            for neighbor in neighbors:
                






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
        minIndex = 0
        for node in self.priorityQueue:
            if dist[node] < dist[minIndex]:
                minIndex = node

        self.priorityQueue.pop(minIndex)
        return minIndex

    def decreasekey(self):
        #  Not needed for the array
        pass

    def isEmpty(self):
        return not self.priorityQueue

#!/usr/bin/python3


from CS312Graph import *
from PriorityQueueArray import *
from BinaryHeap import *
import time
import csv


class NetworkRoutingSolver:
    #create private member that stores computeShortestPath result
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        path_edges = []
        total_length = 0

        end_node = self.network.nodes[destIndex]
        curr_node = end_node

        while curr_node.node_id is not self.source:
            if self.prev[curr_node] is None:
                total_length = float('inf')
                break
            edge = self.edge_between(self.prev[curr_node], curr_node)
            path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
            total_length += edge.length
            curr_node = self.prev[curr_node]

        return {'cost':total_length, 'path':path_edges}


    def edge_between(self, a, b):
        for edge in a.neighbors:
            if edge.dest == b:
                return edge
        return Node

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        #Dijkstra's
        nodeList = self.network
        self.dist = {}
        self.prev = {}
        #use array
        if not use_heap:
            #initialize dist and prev
            for u in nodeList.nodes:
                self.dist[u] = float('inf')
                self.prev[u] = None
            #first node has a dist of 0
            self.dist[nodeList.nodes[self.source]] = 0
            Q = PriorityQueueArray()
            #make queue
            for node in self.dist:
                Q.insert(node, self.dist[node])
            #find the shortest path and update queue
            while len(Q.data) != 0:
                u = Q.delete_min()
                for edge in u.neighbors:
                    v = edge.dest
                    curr_dist = self.dist[u] + edge.length
                    if self.dist[v] > curr_dist:
                        self.dist[v] = curr_dist
                        self.prev[v] = u
                        Q.decrease_key(v, curr_dist)
        else: #binary heap priority queue
            #make queue
            Q = BinaryHeap(nodeList.nodes)
            #inititalize dist, prev, and index (a dictionary that keeps track of the indices in the tree
            for u in nodeList.nodes:
                Q.dist[u] = float('inf')
                Q.prev[u] = None
                Q.index[u] = u.node_id

            #set start node to 0, make sure source node is at beginning of tree
            Q.setup_start_tree(self.source)

            #find shortest paths
            while len(Q.tree_heap) != 0:
                u = Q.delete_min()
                for edge in u.neighbors:
                    v = edge.dest
                    curr_dist = Q.dist[u] + edge.length
                    if Q.dist[v] > curr_dist:
                        Q.dist[v] = curr_dist
                        Q.prev[v] = u
                        Q.decrease_key(v, curr_dist, u)

            self.prev = Q.prev

        t2 = time.time()
        print(t2, '\n')
        with open('output_data.csv', 'a', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow([use_heap, t2 - t1, len(nodeList.nodes)])
        return (t2-t1)


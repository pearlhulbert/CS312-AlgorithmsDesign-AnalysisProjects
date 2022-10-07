#!/usr/bin/python3


from CS312Graph import *
import time
import PriorityQueueArray


class NetworkRoutingSolver:
    #create private member that stores computeShortestPath result
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
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
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        #Dijkstra's
        nodes = self.network.nodes
        edges = self.network.edges
        dist = []
        prev = []
        for _ in self.network:
            dist.append(float('inf'))
            prev.append(None)
        dist[srcIndex] = 0
        queue = make_queue(nodes)
        while len(queue.data) != 0:
            u = queue.delete_min()
            for v in u.neighbors:
                curr_dist = dist[u] + edges[u].length
                if dist[v] > curr_dist:
                    dist[v] = curr_dist
                    prev[v] = u
                    queue.decrease_key(v)
        t2 = time.time()
        return (t2-t1), dist, prev


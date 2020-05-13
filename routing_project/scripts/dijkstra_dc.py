import fiona
import os
import geopandas as gpd

os.chdir(r'C:\Users\14108\Desktop\algorithms\routing_project\data')


class Graph:
    
    #the version I am currently developing requires that the infile is a GPKG
    #layer_name is the name of the target layer in the GPKG
    def __init__(self, infile: str, layer_name: str):
        #get number of nodes so I can start building the adjacency list
        num_nodes = len(fiona.open(infile, layer = 'road_nodes'))
        #the node ids start at 1
        self.nodes = [LinkedList(i + 1) for i in range(0, num_nodes)]
        
        self.adj_list = []
        
        with fiona.open(infile, layer = layer_name) as layer:
            for feature in layer:
                src = feature['properties']['source']
                tgt = feature['properties']['target']
                cost = feature['properties']['cost']
                geom = feature['geometry']
                #adds connection to the adjacency list. i am subtracting one bc
                #the nodes index from one
                self.nodes[src - 1].insert(LinkedList(tgt, cost, geom))
                
                #adds the reverse connection from target to source if it is not
                #a one way street
                if feature['properties']['reverse_cost'] == cost:
                    self.nodes[tgt - 1].insert(LinkedList(src, cost, geom))
                
    #node1 is the integer that represents the start node's gid, node2 is the end node
    def dijkstra(self, node1: int, node2: int):
        #i am storing data on the nodes in a variety of dictionaries. the key is 
        #the node gid and the value is the relevant value (distance, visited, prev_node)
        
        self.df = gpd.GeoDataFrame({'gid': [i.gid for i in self.nodes], 
                                 'distance': [float('inf') for i in self.nodes],
                                 'prev_node': [i.gid for i in self.nodes],
                                 'unvisited': [True for i in self.nodes]})
        #distance from node1 to node1 is 0
        self.df.loc[self.df['gid'] == node1, ['distance']] = 0
        
        #getting the actual objects that represent the nodes
        node1 = self.nodes[node1 - 1]
        node2 = self.nodes[node2 - 1]
        
        self.counter = 0
        while len(self.df[self.df['unvisited'] == True]) > 0:
            self.visitNeighbors()

        
    #iterate through a node's neighbors, determine their distance to the starting node
    #node is a LinkedList object
    def visitNeighbors(self):
        node = self.nodes[self.df[self.df['unvisited'] == True]['distance'].idxmin()]
        tgt_node = node
        
        while tgt_node.next:
            
            neighbor = tgt_node.next
            new_distance = neighbor.cost + self.df[self.df['gid'] == tgt_node.gid]['distance']
            #filter for values that are unvisited, equal the gid we want, and have a higher distance than the new distance
            print(self.df[self.df[self.df[self.df['unvisited'] == True]['gid'] == neighbor.gid]['distance'] > new_distance])
            
            #this part needs some work. time for bed
            if (self.df[self.df['gid'] == neighbor.gid]['unvisited'] == True\
            & self.df[self.df['gid'] == neighbor.gid]['distance']  > new_distance):
                
                self.df.loc[self.df.gid == neighbor.gid, ['distance']] = new_distance
                self.df.loc[self.df.gid == neighbor.gid, ['prev_node']] = tgt_node.gid
                
            #move on to the next neighbor
            tgt_node = neighbor
        #node has been visited
        self.df.loc[self.df.gid == node.gid]['unvisited'] = False
        print(node.gid)


    
#this class is used to build a linked list for each node in the graph
class LinkedList:
    def __init__(self, gid, cost = None, geom = None):
        self.gid = gid
        self.cost = cost
        self.geom = geom
        self.next = None
    #this function adds a new node to the linked list
    def insert(self, node):
        if self.next is None:
            self.next = node
        else:
            self.next.insert(node)
   
graph = Graph('routing_project.gpkg', 'dc_roads')
graph.dijkstra(10, 11)
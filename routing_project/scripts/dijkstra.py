import fiona
from shapely.geometry import shape, LineString
import os
import geopandas as gpd

os.chdir(r'C:\Users\14108\Desktop\algorithms\routing_project\data')


class Graph:
    
    #the version I am currently developing requires that the infile is a GPKG
    #layer_name is the name of the GPKG layer that contains a routable OSM network
    #node_layer is the name of the GPKG layer that contains the nodes of the network
    #cost is the name of the field that will be considered as the cost. in the 
    #osm2po data the code is made for, the 'cost' field is a function of distance 
    #and speed limit. however, there is also a raw distance field titled 'km' that
    #contains length in km
    def __init__(self, infile: str, layer_name: str, node_layer: str, cost_field = 'cost'):
        #get number of nodes so I can start building the adjacency list
        num_nodes = len(fiona.open(infile, layer = node_layer))
        #this dictionary will contain adjacency lists for each node in the network
        self.nodes = {}
        
        #build the dictionary containing node attributes
        with fiona.open(infile, layer = node_layer) as layer:
            for feature in layer:
                node_id = list(feature['properties'].items())[0][1]
                self.nodes[node_id] = LinkedList(node_id, None, shape(feature['geometry']))
                
        with fiona.open(infile, layer = layer_name) as layer:
            for feature in layer:
                src = feature['properties']['source']
                tgt = feature['properties']['target']
                cost = feature['properties'][cost_field]
                geom = shape(feature['geometry'])
                
                #adds connection to the adjacency list.
                self.nodes[src].insert(LinkedList(tgt, cost, geom))
                
                #adds the reverse connection from target to source if it is not
                #a one way street
                if feature['properties']['reverse_cost'] == feature['properties']['cost']:
                    #reverse the geometry of the linestring, makes it easier
                    #down the line to construct the shortest path
                    #I can't reverse this geom while referencing
                    #the original shapely geometry object so it has to be created anew
                    reverse_geom = shape(feature['geometry'])
                    reverse_geom.coords = list(reverse_geom.coords[::-1])
                
                    self.nodes[tgt].insert(LinkedList(src, cost, reverse_geom))
                    

    #node1 is the integer that represents the start node's gid
    #it returns a table that contains all the nodes' distance to the starting node,
    #in addition to attributes that allow the user to retrace the path to the 
    #starting node
    def dijkstra(self, node1: int):
        #i am storing data on the nodes in a variety of dictionaries. the key is 
        #the node gid and the value is the relevant value (distance, visited, prev_node)
        
        self.df = gpd.GeoDataFrame({'gid': [self.nodes[i].gid for i in self.nodes], 
                                 'distance': [float('inf') for i in self.nodes],
                                 'prev_node': [self.nodes[i].gid for i in self.nodes],
                                 'unvisited': [True for i in self.nodes],
                                  'geom': [self.nodes[i].geom for i in self.nodes]}).set_geometry('geom')
        
    
   
        #distance from node1 to node1 is 0
        self.df.loc[self.df['gid'] == node1, ['distance']] = 0
        
        #getting the actual objects that represent the nodes
        self.node1 = self.nodes[node1]

        while len(self.df[self.df['unvisited'] == True]) > 0:
            self.visitNeighbors()
        
        self.df = self.df[self.df['distance'] < float('inf')]
        return self.df

        
    #iterate through a node's neighbors, determine their distance to the starting node
    #node is a LinkedList object
    def visitNeighbors(self):
        #find the index of the smallest distance value in the dataframe 
        min_index = self.df[self.df['unvisited'] == True]['distance'].idxmin()

        node = self.nodes[self.df.iloc[min_index].gid]
        tgt_node = node
        
        while tgt_node.next:
            
            neighbor = tgt_node.next
            new_distance = neighbor.cost + self.df[self.df['gid'] == node.gid]['distance'].values[0]

            #filter for values that are unvisited, equal the gid we want, and have a higher distance than the new distance
            df_gid = self.df[self.df['gid'] == neighbor.gid]
            df_visit = df_gid[df_gid['unvisited'] == True]
            df_dist = df_visit[df_visit['distance'] > new_distance]
            
            #this part needs some work. time for bed
            if len(df_dist) > 0:
                self.df.loc[self.df['gid'] == neighbor.gid, ['distance']] = new_distance
                self.df.loc[self.df['gid'] == neighbor.gid, ['prev_node']] = node.gid
                #setting neighbor geometry equal to geometry from the node to its neighbor 
                #these will later be concatenated when the shortest path is determined
                self.df.loc[self.df['gid'] == neighbor.gid, ['geom']] = neighbor.geom
                                
            #move on to the next neighbor
            tgt_node = neighbor
        #node has been visited
        self.df.loc[self.df['gid'] == node.gid, ['unvisited']] = False


    
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

#df is the return value of the Graph.dijkstra function
#tgt is the gid of the node that you want to reach
def shortestPath(df: Graph.dijkstra, tgt: int):
    #list that will contain linestring geometries that must be concatenated together
    #this will be treated as a stack, in that the last geom added will be the
    #first to be added to the final line segment 
    geoms = []
    coords = []
    
    src = df[df['distance'] == 0]['gid'].values[0]

    while tgt != src:
        geoms.append(df[df['gid'] == tgt]['geom'].values[0])
        tgt = df[df['gid'] == tgt]['prev_node'].values[0]
    
    while len(geoms) > 0:
        seg = geoms.pop()
        seg_coords = list(seg.coords)

        coords += seg_coords

    path = LineString(coords)
    return path

#this function creates a spatial file that contains all the shortest paths
#from a starting node (st_node variable) to all the other nodes in the dataset
def exportShortestPaths(graph: Graph, st_node: int, out_path: str):
    #generate the paths
    paths = graph.dijkstra(st_node)
    gdf = gpd.GeoDataFrame({'gid': [graph.nodes[i].gid for i in paths['gid'].values],
                      'geom': [shortestPath(paths, graph.nodes[i].gid) for i in paths['gid'].values]}).set_geometry('geom')
    gdf.to_file(out_path)
    
# #this generates a graph based on speed limit
# speed_graph = Graph('test_data.gpkg', 'dc_roads', 'road_nodes', cost_field = 'cost')
# #this graph is based specificially on length
# km_graph = Graph('test_data.gpkg', 'dc_roads', 'road_nodes', cost_field = 'km')


# print(shortestPath(km_graph.dijkstra(60288), 57833).wkt)

# exportShortestPaths(speed_graph, 60288, 'speed_dijkstra.shp')
# exportShortestPaths(km_graph, 60288, 'length_dijkstra.shp')

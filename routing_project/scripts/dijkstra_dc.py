import fiona
import os

os.chdir(r'C:\Users\14108\Desktop\algorithms\routing_project\data')


class Graph:
    
    #the version I am currently developing requires that the infile is a GPKG
    #layer_name is the name of the target layer in the GPKG
    def __init__(self, infile: str, layer_name: str):
        self.nodes = []
        self.adj_list = []
        
        with fiona.open(infile, layer=layer_name) as layer:
            for feature in layer:
                self.nodes.append(feature['properties']['source'])
                self.nodes.append(feature['properties']['target'])
        
        self.nodes = list(dict.fromkeys(self.nodes))
        self.nodes.sort()
        print(len(self.nodes))
    
#this class is used to build a linked list for each node in the graph
class LinkedList:
    def __init__(self, id):
        self.id = id
        self.next = None
   
graph = Graph('routing_project.gpkg', 'dc_roads')
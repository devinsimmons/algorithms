# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 18:00:42 2019

@author: Devin Simmons
"""

#class for each node of the linked list the the deque is built on
class Node:
    def __init__(self, data, next_nd = None):
        self.data = data
        self.next_nd = next_nd
    def findNext(self):
        return self.next_nd
#a deque, which is essentially a queue where the client can insert and remove data
#at both the front and the back of the data structure. Deque is short for double 
#ended queue
class Deque:
    
    #start off with empty start node
    def __init__(self, data = None):
        self.start = Node(data)
        
        #store items in a list that allows client to see the contents of the deque
        if data:
            self.content = [data]
        else:
            self.content = []
        
    #function that returns the last item in the deque. works in linear time
    def lastNode(self, node = None):
        
        if not node:
            node = self.start
        #if there is no next node, then the end has been reached
        if node.data and not node.next_nd:
            return node
        
        try:
            if not self.isEmpty():
                return self.lastNode(node.next_nd) 
        except:
            raise ValueError('The deque is empty')
                
            
    #returns whether the deque is empty
    def isEmpty(self):
        return not self.start.data
    
    
    #pushes new data to the front
    def pushFront(self, data):
        #puts data in start node if the deque is empty
        if self.isEmpty():
            self.start.data = data
        
        else:
            self.oldStart = self.start
            self.start = Node(data, self.oldStart)
        
        self.content = [data] + self.content
    #pushes new data to the back
    def pushEnd(self, data):
        if self.isEmpty():
            self.start.data = data
        else:
            self.lastNode().next_nd = Node(data)
        
        self.content.append(data)
            
    #remove first item from deque
    def popFront(self):
        if self.start.next_nd:
            self.start = self.start.next_nd
            self.content = self.content[1:]
        else:
            self.start.data = None
            self.content = []
       
    #remove last item from deque
    def popEnd(self, node = None):
        if not node:
            node = self.start
            
        if node.next_nd:
            if self.popEnd(node.next_nd):
                #remove connection to the last node
                node.next_nd = None
                
        else:
            self.content = self.content[:-1]
            return True
        
test = Deque(1)
test.pushFront(2)
test.pushEnd(3)
test.pushFront(4)
test.popFront()
test.popFront()
print(test.content)

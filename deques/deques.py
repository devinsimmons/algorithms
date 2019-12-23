#class for each node of the linked list the the deque is built on
class Node:
    def __init__(self, data, next_nd = None, last = None):
        self.data = data
        self.next_nd = next_nd
        self.last = last
    def findNext(self):
        return self.next_nd
#a deque, which is essentially a queue where the client can insert and remove data
#at both the front and the back of the data structure. Deque is short for double 
#ended queue
class Deque:
    
    #start off with empty start node
    def __init__(self, data = None):
        self.start = Node(data)
        #self.end will equal none if the list is empty or has only one node
        self.end = None
        #store items in a list that allows client to see the contents of the deque
        if data:
            self.content = [data]
        else:
            self.content = []
            
    #returns whether the deque is empty
    def isEmpty(self):
        return not self.start.data
    
    
    #pushes new data to the front
    def pushFront(self, data):
        #puts data in start node if the deque is empty
        if self.isEmpty():
            self.start.data = data
        
        else:
            oldStart = self.start
            self.start = Node(data, oldStart)
            oldStart.last = self.start
            
            if not self.end:
                self.end = oldStart
                
        
        self.content = [data] + self.content
    #pushes new data to the back
    def pushEnd(self, data):
        if self.isEmpty():
            self.start.data = data
        else:
            if self.end:
                oldEnd = self.end
                self.end = Node(data, None, oldEnd)
                oldEnd.next_nd = self.end
            else:
                self.end = Node(data, self.start, None)
        self.content.append(data)
            
    #remove first item from deque
    def popFront(self):
        if self.isEmpty():
            raise ValueError('the deque is already empty')
        else:
            if self.start.next_nd:
                self.start = self.start.next_nd
                self.start.last = None
                self.content = self.content[1:]
            else:
                self.start.data = None
                self.content = []
       
    #remove last item from deque
    def popEnd(self):
        if self.isEmpty():
            raise ValueError('the deque is already empty')
        else:
            self.end = self.end.last
            self.end.next_nd = None
            self.content = self.content[0:-1]
    
    def contents(self, node = None):
        
        if not node:
            node = self.start
        
        if node.next_nd:
            return [node.data] + self.contents(node.next_nd)
        else:
            return [node.data]
        

import random
import time

start = time.time()

test = Deque()
test.pushFront(1)
test.pushFront(3)

test.pushFront(5)
test.pushFront(6)
test.popFront()
test.popEnd()
print(test.contents())
test.pushEnd(6)
test.pushEnd(7)
test.popEnd()
test.pushFront(1)
print(test.start.data, test.end.data, test.end.last.data, test.start.next_nd.data)
print(test.contents())
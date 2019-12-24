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

            
    #returns whether the deque is empty
    def isEmpty(self):
        return not self.start.data
    
    
    #pushes new data to the front
    def pushFront(self, data):
        #puts data in start node if the deque is empty
        if not self.isEmpty():
            oldStart = self.start
            self.start = Node(data, oldStart)
            oldStart.last = self.start
            
            if not self.end:
                self.end = oldStart
            
        else:
            self.start.data = data
                
    
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
        
    #remove first item from deque
    def popFront(self):
        if self.isEmpty():
            raise ValueError('the deque is already empty')
        else:
            if self.start.next_nd:
                self.start = self.start.next_nd
                self.start.last = None
            else:
                self.start.data = None

       
    #remove last item from deque
    def popEnd(self):
        if self.isEmpty():
            raise ValueError('the deque is already empty')
        else:
            self.end = self.end.last
            self.end.next_nd = None
    
    def contents(self, node = None):
        
        if not node:
            node = self.start
        
        if node.next_nd:
            return [node.data] + self.contents(node.next_nd)
        else:
            return [node.data]
        
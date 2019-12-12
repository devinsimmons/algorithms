#implementation of percolation algorithm
 
class Percolation:
    
    #n represents the number of cells that will be in the grid. n must be
    #a perfect square
    def __init__(self, n: int):
        self.n = n
        
        try:
            if int(int(n**0.5) * (n**0.5)) != int(n):
                raise ValueError('Constructor argument must be a perfect square')
        except(TypeError):
            exit('Input must be an integer')
        
        self.num_rows = int(n**0.5)
        #create a grid with n cells, plus a cell at the top and a cell at the bottom
        #the grid starts off with all cells closed (closed is represented by 0), 
        #except the top and bottom cells
        self.grid = [0 for i in range(0, n + 2)]
        self.grid[0] = 1
        self.grid[n + 1] = 1
        
        #list describes the parent cell for each cell
        #value given is the index of the parent cell
        #setting parents for top and bottom rows equal to the virtual cells
        self.grid_id = [0] * (self.num_rows + 1)
        self.grid_id += [i for i in range(self.num_rows + 1, (n + 1) - self.num_rows)]
        self.grid_id += [n + 1] * (self.num_rows + 1)
        
        #array that tracks how long each tree rooted at the index is 
        self.sz = [0 for i in range (0, n + 2)]
        
    
    #converts coordinates for rows and columns to a single integer index value
    #the grid starts with 1 in the top left, ends with n in the bot right
    #the indexes from 1 because the virtual point at the top is index 0
    #however columns and rows still index from 0
    def translate(self, row: int, col: int):
        #case for the top virtual cell
        if row == -1 and col == -1:
            return 0
        #case for the bottom virtual cell
        elif row == self.num_rows and col == self.num_rows:
            return self.n + 1
        else:
            return (1 + row*self.num_rows + col) 
    
    #checks if cell exists given row and column indices
    #handle edge cases where cells are literally on the edge of the grid
    #and don't have four adjacent cells
    def cellExists(self, row: int, col: int):
        if (row < 0 or row >= self.num_rows) or (col < 0 or col >= self.num_rows):
            return False
        else:
            return True
        
    #opens a cell if it is not already open
    def openCell(self, row: int, col: int):
        if not self.isOpen(row, col):
            #opens the cell
            self.grid[self.translate(row, col)] = 1
            
            #check if adjacent cells are connected. if not, perform a union
            adj_cells = [(row + 1, col), (row, col + 1),
                         (row - 1, col), (row, col - 1)]
            
            for cell in adj_cells:
                if self.cellExists(cell[0], cell[1]) and self.isOpen(cell[0], cell[1]):
                    
                    self.union(row, col, cell[0], cell[1])
                
    #returns boolean that indicates whether cell is open
    def isOpen(self, row: int, col: int):
        return(bool(self.grid[self.translate(row, col)]))
    
    #returns number of cells that are open
    def numberOfOpenCells(self):
        #subtracts 2 because it shouldn't count the virtual cells I created\
        return(sum(self.grid) - 2)
    
    #check if two cells are connected
    def isConnected(self, rowp: int, colp: int, rowq:int, colq:int):
        return self.findRoot(self.translate(rowp, colp)) == self.findRoot(self.translate(rowq, colq))
          
    #function that determines the length of each tree. this is used to make union
    #more efficient, because linking shorter trees to the root of the taller tree
    #reduces the number of traversals necessary
    #function is called each time a root is found. result is used to do a weighted
    #union (more shallow tree is attached to the root of the deeper tree)
    #currently treeSize is making the algorithm 10 times slower
    #i need to fix tree size and find a more efficient way of calculating it
    def treeSize(self, index):
        #return self.sz[self.findRoot[index]]
        #find the indices of the root node's direct children
        children = [i for i in range(0, len(self.grid_id)) if self.grid_id[i] == index
                    and i != index]
        if len(children) > 0: 
            for i in children:
                return len(children) + self.treeSize(i)
        else:
            return len(children)
        
    #function that creates union between components, if they are both adjacent
    #and open
    #i need to work on path compression
    def union(self, rowp: int, colp: int, rowq: int, colq: int):
        if not self.isConnected(rowp, colp, rowq, colq):
            #performs path compression
            if self.treeSize(self.translate(rowp, colp)) > self.treeSize(self.translate(rowq, colq)):
                self.grid_id[self.findRoot(self.translate(rowq, colq))] = self.findRoot(self.translate(rowp, colp))
            else:
                self.grid_id[self.findRoot(self.translate(rowp, colp))] = self.findRoot(self.translate(rowq, colq))
                
                
    #function that is executed by isConnected to find the root of an object
    #index should be the index of the cell in the array data structures
    def findRoot(self, index):
        if self.grid_id[index] == index:
            #update the size of the root
            self.sz[index] = self.treeSize(index)
            return index
        else:
            #continue traversing the tree until the index of the root node is reached
            return self.findRoot(self.grid_id[index])
    #returns true if the grid percolates
    def percolates(self):
        #check if the virutal cells are connected
        return self.isConnected(-1, -1, self.num_rows, self.num_rows)
          

import random
import time

def testPercolation(n):
    test = Percolation(n)
    
    for i in range(0, n * 10):
        x = random.randint(0, (n**0.5) - 1)
        y = random.randint(0, (n**0.5) - 1)
        test.openCell(x, y)
        if test.percolates():
            return(test.numberOfOpenCells())


result = 0
start_time = time.time()
for i in range(0, 10):
    result += testPercolation(400)
print(time.time() - start_time)    
print(result/100)


#implementation of percolation algorithm
 
class Percolation:
    
    #n represents the number of cells that will be in the grid. n must be
    #a perfect square
    def __init__(self, n: int):
        
        try:
            if int(int(n**0.5) * (n**0.5)) != int(n):
                raise ValueError('Constructor argument must be a perfect square')
        except(TypeError):
            exit('Input must be an integer')
        
        #create a grid with n cells, plus a cell at the top and a cell at the bottom
        self.grid = [i for i in range(0, n + 2)]
            
test = Percolation('hi')
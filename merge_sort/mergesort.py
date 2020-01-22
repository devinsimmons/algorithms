import random
import matplotlib.pyplot as plt
#mergesort can work on lists of number values (integers or floats)
#it sorts from least value to greatest value
class MergeSort:
    
    def __init__(self, arr: list):
        self.arr = arr
    
    #determines order of sorting
    def msort(self, how = 'low_to_high'):
        if how == 'low_to_high':
            return self.order(self.arr)
        elif how == 'high_to_low':
            sort_obj = HighToLow(self.arr)
            return sort_obj.order(sort_obj.arr)
            
    #function that recursively calls the merge function on subarrays
    def order(self, arr):
        mid = len(arr) //2 + 1
        #array of length 1
        if mid < 2:
            return arr
        
        
        #arrs length 2
        elif len(arr) == 2:
            return self.merge([arr[0]], [arr[1]])
        else:
            arr1 = self.order(arr[0:mid])
            arr2 = self.order(arr[mid:])
            return self.merge(arr1, arr2)            
    
    #this function compares two values to determine insertion order
    def comparator(self, obj1, obj2):
        return obj1 < obj2
    
    #merges two sorted arrays
    def merge(self, arr1, arr2):
        #faster to start with empty list than a list of length n
        new_arr = []
        #index of the first arr  
        i = 0
        #index of the second arr
        j = 0
        
        #do quick merge, compare entry from left list to right list, put lower 
        ##value in the new arr
        for x in range(0, (len(arr1) + len(arr2))):
            #essentially says if arr1[i] < arr2[j]
            if self.comparator(arr1[i], arr2[j]):
                new_arr.append(arr1[i])
                if (i+1) < len(arr1):
                    i += 1
                    
                #add remaining list to the end
                else:
                    new_arr += arr2[j:]
                    break
            else:
                new_arr.append(arr2[j])
                if (j+1) < len(arr2):
                    j += 1
                else:
                    new_arr += arr1[i:]
                    break
        return new_arr
    
    
            
    

#class that orders the list from high to low. 
class HighToLow(MergeSort):
    
    #changes basis for comparison
    def comparator(self, obj1, obj2):
        return obj1 > obj2

#class that orders coordinates based on x coord, ties broken based on y coord
class MergeSortCoords(MergeSort):
    
    def comparator(self, obj1, obj2):
        if obj1[0] == obj2[0]:
            return obj1[1] > obj2[1]
        else:
            return obj1 > obj2

#class that applies mergesort to points, ordering them by the slope they have
#to another point
class MergeSortSlopes(MergeSort):
    
    def __init__(self, arr: list, pt):
        self.arr = arr
        #create point object that is the basis of all comparisons made in the 
        #modified merge function
        #can take either a tuple of coords or a pt object
        if type(pt) == tuple:
            self.pt = Point(pt)
        else:
            self.pt = pt
    
    #comparison is now made between slopes
    def comparator(self, obj1, obj2):
        slope1 = self.pt.calcSlope(Point(obj1))
        slope2 = self.pt.calcSlope(Point(obj2))
        
        return slope1 < slope2
    
#point class (x and y coordinates)   
class Point:
    
    def __init__(self, coords: tuple):
        self.x = coords[0]
        self.y = coords[1]
    
    #point should be an instance of the point class
    def calcSlope(self, point):
        #handle undefined slope
        if self.x == point.x and self.y != point.y:
            return float('inf')
        #handle situation where both points are equal
        elif self.y == point.y and self.x == point.x:
            return -float('inf')
        #normal slope equation
        return (self.y - point.y)/(self.x - point.x)
    
#contstructing the line segments. in this case, a line segment requires at least
#3 collinear points
#points should just be normal tuples
class LineSegment:
    def __init__(self, pt1, pt2, pt3, pt4):
        self.pts = [pt1, pt2, pt3, pt4]
        self.slope = Point(pt1).calcSlope(Point(pt2))
        
    def addPoint(self, pt):
        self.pts.append(pt)
        
    
    


#function that detects, and returns, any line segments with more than 3 points
#when passed a list of tuples 
def detectLines(pts):
    #store line segment objects that are generated
    lines = []
    
    for i in pts:
        line = None 
        pt = Point(i)
        #sort the points based on their slopes
        pts = MergeSortSlopes(pts, pt).msort()
        
        
        for x in range(2, len(pts)):
            #skip duplicate points
            if pts[x] == i:
                pass
            #check if the point matches the current line being constructed, if 
            #one exists
            elif line:
                if pt.calcSlope(Point(pts[x])) == line.slope:
                    line.addPoint(pts[x])
                #reset line if slope doesn't match
                else:
                    if compareLineSlopes(lines, line):
                        lines.append(line)
                    line = None
            #if the slope of two consecuitve points are equal, a line segment exists
            #and is initiated
            else:
                
                if pt.calcSlope(Point(pts[x])) ==  pt.calcSlope(Point(pts[x - 1])) \
                and pt.calcSlope(Point(pts[x])) ==  pt.calcSlope(Point(pts[x - 2])):
                    line = LineSegment(i, pts[x-1], pts[x-2], pts[x])

                if x == len(pts) - 1 and line:
                    if compareLineSlopes(lines, line):
                        lines.append(line)
    return lines

#function that makes sure that repeat lines are not being added
#returns true if the slope of the new line is not in the list of lines
def compareLineSlopes(lines, targetLine):
    for line in lines:
        if line.slope == targetLine.slope:
            return False
    #puts the points in correct drawing order
    targetLine.pts = MergeSortCoords(targetLine.pts).msort()
    return True
    

#creating a matplotlib visualizer that inputs random coordinates, draws a new 
#frame each time a point is added, and then draws lines as they appear
def visualizer(num_pts, outpath, max_coord = 30):
    pts = []
    lines = []
    for i in range(0, num_pts):
        pts.append((random.randint(0, max_coord), random.randint(0, max_coord)))
        lines += detectLines(pts)
        plt.scatter([x[0] for x in pts], [y[1] for y in pts])
        for i in lines:
            plt.plot([x[0] for x in i.pts], [y[1] for y in i.pts], color = 'green')
            plt.scatter([x[0] for x in i.pts], [y[1] for y in i.pts], color = 'green')
        
#        plt.xlim(max_coord)
#        plt.ylim(max_coord)
        plt.show()
visualizer(45, None)
        
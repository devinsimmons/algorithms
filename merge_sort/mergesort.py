import operator
import matplotlib.pyplot as plt
#mergesort can work on lists of number values (integers or floats)
#it sorts from least value to greatest value
class MergeSort:
    
    def __init__(self, arr: list):
        self.arr = arr
    
    #determines order of sorting
    def sort(self, how = 'low_to_high'):
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
    

    #merges two sorted arrays
    def merge(self, arr1, arr2, op = operator.lt):
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
            if op(arr1[i], arr2[j]):
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
    
    #merges two sorted arrays, ordering from high to low
    #the operator is switched to be >
    def merge(self, arr1, arr2):
        #changes the default arg for op
        return super().merge(arr1, arr2, op = operator.gt)

#point class    
class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    #point should be an instance of the point class
    def calcSlope(self, point):
        return (self.y - point.y)/(self.x - point.x)
    
    
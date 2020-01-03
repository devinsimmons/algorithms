#mergesort can work on lists of number values (integers or floats)
#it sorts from least value to greatest value
class MergeSort:
    
    def __init__(self, arr: list):
        self.arr = arr
        self.arr.mergeSort()
    
    def mergeSort(self):
        mid = len(self.arr) //2 + 1
        if mid < 2:
            return self.arr
        
        
        arr1 = MergeSort.merge(self.arr[0:mid])
        arr2 = MergeSort.merge(self.arr[mid:])
        
        return MergeSort.merge(arr1, arr2)            
    

    #merges two sorted arrays
    @staticmethod
    def merge(arr1, arr2):
        new_arr = [0] * len(arr1) + [0] * len(arr2)
        
        #index of the first arr  
        i = 0
        #index of the second arr
        j = 0
        #index of the final arr
        k  = 0
        
        #do quick merge, compare entry from left list to right list, put lower 
        ##value in the new arr
        for x in range(0, len(new_arr)):

            if arr1[i] < arr2[j]:
                new_arr[k] = arr1[i]
                if (i+1) < len(arr1):
                    i += 1
                #add remaining list to the end
                else:
                    new_arr[k+1:] = arr2[j:]
                    break
            else:
                new_arr[k] = arr2[j]
                if (j+1) < len(arr2):
                    j += 1
                else:
                    new_arr[k+1:] = arr1[i:]
                    break
            k += 1
        return new_arr
    
print(MergeSort.merge([1, 9, 11], [2, 12, 13]))        
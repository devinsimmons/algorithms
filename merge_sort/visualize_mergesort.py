#mergesort can work on lists of number values (integers or floats)
#it sorts from least value to greatest value
class MergeSort:
    
    def __init__(self, arr: list):
        self.arr = arr
    
    def sort(self, how = 'low_to_high'):
        if how == 'low_to_high':
            return MergeSort.order(self.arr)
    
    @staticmethod
    def order(arr):
        mid = len(arr) //2 + 1
        #array of length 1
        if mid < 2:
            return arr
        
        
        #arrs length 2
        elif len(arr) == 2:
            return MergeSort.merge([arr[0]], [arr[1]])
        else:
            arr1 = MergeSort.order(arr[0:mid])
            arr2 = MergeSort.order(arr[mid:])
            return MergeSort.merge(arr1, arr2)            
    

    #merges two sorted arrays
    @staticmethod
    def merge(arr1, arr2):
        #faster to start with empty list than a list of length n
        new_arr = []
        #index of the first arr  
        i = 0
        #index of the second arr
        j = 0
        
        #do quick merge, compare entry from left list to right list, put lower 
        ##value in the new arr
        for x in range(0, (len(arr1) + len(arr2))):

            if arr1[i] < arr2[j]:
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

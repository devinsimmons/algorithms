#file to test the mergesort
import unittest
import visualize_mergesort as vm
import random

class TestMergesort(unittest.TestCase):
    
    def setUp(self):
        #makes list of 100 random integers that have values between 0 and 100 
        self.arr = [random.randrange(0, 100) for i in range(0, 100)]
        self.sorted_arr = vm.MergeSort(self.arr).sort()
        self.testOrder()
    
    #check each entry in the sorted list and make sure that it is less than or
    #equal to the next entry
    def testOrder(self):
        for i in range(0, len(self.sorted_arr)):
            if i == len(self.sorted_arr) - 1:
                break
            else:
                self.assertTrue(self.sorted_arr[i + 1] >= self.sorted_arr[i])
        
        

if __name__ == "__main__":
    unittest.main()
        
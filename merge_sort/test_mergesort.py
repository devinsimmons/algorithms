#file to test the mergesort
import unittest
import visualize_mergesort as vm
import random

class TestMergesort(unittest.TestCase):
    
    def setUp(self):
        #makes list of 100 random integers that have values between 0 and 100 
        self.arr = [random.randrange(0, 100) for i in range(0, 100)]
        self.sorted_arr_low = vm.MergeSort(self.arr).sort()
        self.arr_high = vm.MergeSort(self.arr).sort('high_to_low')
        self.testOrderLow()
        self.testOrderHigh()
    
    #check each entry in the low to high sorted list and make sure that it is less than or
    #equal to the next entry
    def testOrderLow(self):
        
        for i in range(0, len(self.sorted_arr_low)):
            if i == len(self.sorted_arr_low) - 1:
                break
            else:
                self.assertTrue(self.sorted_arr_low[i + 1] >= self.sorted_arr_low[i])
                
    
    #testing the order of the high to low array
    def testOrderHigh(self):
        for i in range(0, len(self.arr_high)):
            if i == len(self.arr_high) - 1:
                break
            else:
                self.assertTrue(self.arr_high[i+1] <= self.arr_high[i])
        

if __name__ == "__main__":
    unittest.main()
        
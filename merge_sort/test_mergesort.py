#file to test the mergesort
import unittest
import mergesort as vm
import random

class TestMergesort(unittest.TestCase):
    
    def setUp(self):
        #makes list of 100 random integers that have values between 0 and 100 
        self.arr = [random.randrange(0, 100) for i in range(0, 100)]
        self.sorted_arr_low = vm.MergeSort(self.arr).msort()
        self.arr_high = vm.MergeSort(self.arr).msort('high_to_low')
        #creates 100 points with random coordinates
        self.pts = [(random.randint(0, 100), random.randint(0, 100)) for i in range (0, 100)]
        
        self.testCoordsOrder()
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
    
    #tests the mergeSortCoords class, makes sure that the coords are being sorted
    #high to low based on x coord with ties broken  by the y coord
    def testCoordsOrder(self):
        ordered_coords = vm.MergeSortCoords(self.pts).msort()

        for i in range(0, len(ordered_coords)):
            if i == len(ordered_coords) - 1:
                break
            else:
                if ordered_coords[i+1][0] == ordered_coords[i][0]:
                    self.assertTrue(ordered_coords[i+1][1] <= ordered_coords[i][1])
                else:
                    self.assertTrue(ordered_coords[i+1][0] <= ordered_coords[i][0])
            
    #tests that slopes to a point at 1, 1 are being returned in the order low to high
    def testSlopeOrder(self):
        pt = vm.Point((1, 1))
        ordered_slopes = vm.MergeSortSlopes(self.pts, pt).msort()
        
        for i in range(0, len(ordered_slopes)):
            if i == len(ordered_slopes) - 1:
                break
            else:
                pt1 = vm.Point(ordered_slopes[i+1])
                pt2 = vm.Point(ordered_slopes[i])
                self.assertTrue(pt.calcSlope(pt1) >= pt.calcSlope(pt2))

if __name__ == "__main__":
    unittest.main()
        
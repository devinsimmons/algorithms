import deques as dq
import unittest

class TestDeque(unittest.TestCase):
    
    def setUp(self):
        self.deque = dq.Deque()
    
    #test push methods
    def testPush(self):
        self.deque.pushFront(1)
        self.deque.pushFront(2)
        self.deque.pushFront(5)
        self.deque.pushFront(6)
        self.deque.pushFront(7)
        self.deque.pushEnd(4)
        self.deque.pushEnd(3)
        
        self.assertEqual(self.deque.contents(), [7, 6, 5, 2, 1, 4, 3])
    
    def testPop(self):
        self.testPush()
        self.deque.popFront()
        self.deque.popEnd()
        self.assertEqual(self.deque.contents(), [6, 5, 2, 1, 4])
        
        self.deque.pushEnd(3)
        self.deque.popFront()
        self.assertEqual(self.deque.contents(), [5, 2, 1, 4, 3])
    
    
if __name__ == "__main__":
    unittest.main()
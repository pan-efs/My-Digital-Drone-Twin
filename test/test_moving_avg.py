from unittest import TestCase
from filters.moving_average import MovingAverage as MovingAverage

class TestMovingAverage(TestCase):
    
    def test_moving_average(self):
        m = MovingAverage()
        arr = [1, 2, 3]
        f = m.moving_average(arr, 2)
        self.assertEqual(1.5, f[0]) # Due to ambiguity
        
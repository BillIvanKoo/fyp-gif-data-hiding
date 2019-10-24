import unittest
from preprocess import *
from gif import Gif

path = "D:\Monash\FIT3162\GIF collection\circle.gif"
inputgif = Gif.from_file(path)

class Test_Preprocess(unittest.TestCase):
    def setUp(self):
        pass

    def test_capacity(self):
        self.assertGreater(count_available_storage(inputgif), 0, "")

if __name__ == '__main__':
    unittest.main()
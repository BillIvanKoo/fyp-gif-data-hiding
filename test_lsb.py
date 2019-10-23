import unittest
from gif import Gif
from lsb_gif import *
# Author : Jia Qin Choong
# Usage: Testing functions of lsb_gif.py (main functionality)

path = "D:\Monash\FIT3162\GIF collection\levi.gif"
inputgif = Gif.from_file(path)

class Test_lsb_gif(unittest.TestCase):
    def test_encode(self):
        message = "This is test message number 1"
        cap = len(message)
        encode(cap,message,inputgif)
        result = decode(inputgif)
        self.assertEqual(message,result,"Failed to encode GIF")

    def test_decode(self):
        message = "This is test message number 2"
        cap = len(message)
        encode(cap,message,inputgif)
        result = decode(inputgif)
        self.assertEqual(message,result,"Failed to decode GIF")

if __name__ == '__main__':
    unittest.main()
import unittest
from encode_gif import *
from decode_gif import *
from gif import Gif

# Author : Jia Qin Choong
# Usage: Testing functions of decode_gif.py (encoding in a color table)
path = "D:\Monash\FIT3162\GIF collection\levi.gif"
inputgif = Gif.from_file(path)
gct = inputgif.global_color_table.entries
msg = "testmessage2"
lsb_encode(msg, gct)

class Test_DeodingGIF(unittest.TestCase):
    def test_lsb_decode(self):
        res = lsb_decode(gct)
        self.assertEqual(msg,res, "Failed to decode from GCT")

if __name__ == '__main__':
    unittest.main()
import unittest
from encode_gif import *
from decode_gif import *
from gif import Gif

# Author : Jia Qin Choong
# Usage: Testing functions of encode_gif.py (encoding in a color table)
path = "D:\Monash\FIT3162\GIF collection\levi.gif"
inputgif = Gif.from_file(path)

class Test_EncodingGIF(unittest.TestCase):
    def test_lsb_encode(self):
        # Purpose of the test is to see if the bits are encoded in the GIF properly
        gct = inputgif.global_color_table.entries
        msg = "testmessage1"
        lsb_encode(msg, gct)
        result = lsb_decode(gct)
        self.assertEqual(msg, result, "Failed to encode")

if __name__ == '__main__':
    unittest.main()
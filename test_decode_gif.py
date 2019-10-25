import unittest
from encode_gif import *
from decode_gif import *
from gif import Gif

# Author : Jia Qin Choong
# Usage: Testing functions of decode_gif.py (decoding in a color table)
path = "./test_src/levi.gif"
inputgif = Gif.from_file(path)

class Test_DecodingGIF(unittest.TestCase):
    def test_lsb_decode(self):
        gct = inputgif.global_color_table.entries
        msg = "testmessage2"
        lsb_encode(msg, gct)
        res = lsb_decode(gct)
        self.assertEqual(msg,res, "Failed to decode from GCT")

if __name__ == '__main__':
    unittest.main()
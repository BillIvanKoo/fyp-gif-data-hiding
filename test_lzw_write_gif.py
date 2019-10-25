"""
Filename: test_lzw_write_gif.py
Author: Bill Ivan Kooslarto - 28694120
Tested both LZW compression, decompression and writing into a file
"""
import unittest
from gif import Gif
from image_data_lzw import *
from kaitai_gif_write import *

class TestLZWWriteGif(unittest.TestCase):
    def setUp(self):
        # set up with small gif file and known index values
        self.gif = Gif.from_file("./test_src/sample_1.gif")
        self.indexes = ['1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '1', '1', '1', '0', '0', '0', '0', '2', '2', '2', '1', '1', '1', '0', '0', '0', '0', '2', '2', '2', '2', '2', '2', '0', '0', '0', '0', '1', '1', '1', '2', '2', '2', '0', '0', '0', '0', '1', '1', '1', '2', '2', '2', '2', '2', '1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '1', '1', '1', '1', '1']
    
    def test_gif_to_bytearray(self):
        # test that gif turn to byte array 
        res = gif_to_bytearray(self.gif)
        self.assertIsInstance(res, bytearray)
    
    def test_write_to_file(self):
        # test that writing to file does not change the gif
        write_to_file(self.gif, "./test_src/res_1.gif")
        res_gif = Gif.from_file("./test_src/res_1.gif")
        self.assertEqual(gif_to_bytearray(self.gif), gif_to_bytearray(res_gif))


    def test_decode(self):
        # test that decoding/decompressing return the right indexes
        for i in self.gif.blocks:
            if i.block_type == Gif.BlockType.local_image_descriptor:
                resulting_index = decode(i.body.image_data)
                self.assertEqual(resulting_index, self.indexes)

    def test_encode1(self):
        # test the encoded/compressed indexes that it is the same as earlier
        new_subblocks = encode(self.indexes)
        for i in new_subblocks:
            self.assertIsInstance(i, Gif.Subblock)
        for i in self.gif.blocks:
            if i.block_type == Gif.BlockType.local_image_descriptor:
                i.body.image_data.subblocks.entries = new_subblocks
        
        gif2 = Gif.from_file("./test_src/sample_1.gif")

        self.assertEqual(gif_to_bytearray(self.gif), gif_to_bytearray(gif2))
    
    def test_encode2(self):
        # test that changing the indexes and compressing it will still work
        self.indexes[0] = '2'
        self.indexes[6] = '1'
        new_subblocks = encode(self.indexes)
        for i in self.gif.blocks:
            if i.block_type == Gif.BlockType.local_image_descriptor:
                i.body.image_data.subblocks.entries = new_subblocks
        
        write_to_file(self.gif, "./test_src/res_2.gif")
        gif2 = Gif.from_file("./test_src/res_2.gif")

        for i in gif2.blocks:
            if i.block_type == Gif.BlockType.local_image_descriptor:
                resulting_index = decode(i.body.image_data)
                self.assertEqual(resulting_index, self.indexes)
        

if __name__ == '__main__':
    unittest.main()
import unittest
from preprocess import *
from gif import Gif
# Author : Jia Qin Choong
# Usage : Testing functions in preprocess.py

path = "D:\Monash\FIT3162\GIF collection\levi.gif"
inputgif = Gif.from_file(path)

class Test_Preprocess(unittest.TestCase):
    def test_capacity(self):
        # check to see if the count returned a value > 0
        self.assertGreater(count_available_storage(inputgif), 0, "Failed to check capacity")

    def test_get_lct_index(self):
        # check to see  if the number of frames are obtained properly
        indexlist = get_lct_index(inputgif)
        blocks = inputgif.blocks
        count = 0
        for i in range(len(blocks)):
            if str(blocks[i].block_type) == "BlockType.local_image_descriptor":
                count += 1
        self.assertEqual(len(indexlist), count, "Failed to get lct index list")

    def test_setlocalCT(self):
        # check if all the local color table flag has been set to 135
        indexlist = set_local_color_table(inputgif)
        count = 0
        blocks = inputgif.blocks  # the frames are stored in blocks

        for i in range(1, len(indexlist)):
            index = indexlist[i]
            if blocks[index].body.flags == 135:  # more than 0 if there is a local color table
                count += 1
        # len - 1 because the first frame will not be changed or checked for
        self.assertEqual(len(indexlist)-1, count, "Failed to set local color table")

    def test_copy_gct(self):
        table = copy_global_ct(inputgif)
        self.assertEqual(len(table.entries), 256, "Failed to copy GCT")

    def test_check_gct(self):
        # checks if the inputGIF contains a GCT
        checkGCT(inputgif)
        flag = inputgif.logical_screen_descriptor.flags
        self.assertNotEqual(flag & 135, 0, "Failed check GCT")

if __name__ == '__main__':
    unittest.main()
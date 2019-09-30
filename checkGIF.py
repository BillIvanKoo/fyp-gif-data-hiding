from gif import Gif
from kaitai_gif_demo import *
import os, glob

def copy_global_ct(inputgif):
    """
    This function creates a copy of the global colour table
    :param inputgif: the input gif object
    :return: new table which is a deep copy of the global color table
    """
    global_table = inputgif.global_color_table
    new_table = Gif.ColorTable(global_table._io)
    for i in global_table.entries:
        newcolor = Gif.ColorTableEntry(None)
        newcolor.red = i.red
        newcolor.green = i.green
        newcolor.blue = i.blue
        new_table.entries.append(newcolor)
    return new_table

def set_local_color_table(inputgif):
    blocks = inputgif.blocks
    indexlist = []
    # get all the indices of frames of a gif
    for i in range(len(blocks)):
        if str(blocks[i].block_type) == "BlockType.local_image_descriptor":
            indexlist.append(i)

    for i in range(1,len(indexlist)):
        index = indexlist[i]
        if blocks[index].body.flags > 0:                     # more than 0 if there is a local color table
            pass

        else:                                               # 0 if there is no local color table
            blocks[index].body.flags = 135                    # set the flag to more than 0 to indicate there is color table
            new_table = copy_global_ct(inputgif)
            inputgif.blocks[index].body.local_color_table = new_table

    return indexlist

def count_available_storage(inputgif):
    """
    A function to count how many characters can be stored in the GIF
    :param inputgif: The target GIF object
    :return: total number of characters to be stored in the GIF
    """
    # global colour table available storage
    count = 255 * 3                                       # 1 entry is used as an indicator of how many characters are stored
    frames = len(set_local_color_table(inputgif)) - 1     # number of frames available, not including the first frame
    count += 255 * 3 * frames               # total number of bits to be stored
    count = count // 8                      # divide by each 8-bit ASCII to get character count
    return count

if __name__ == "__main__":
    # check all the GIFs for the last entry in the global colour table
    path = "D:\Monash\FIT3162\GIF collection"
    """
    for filename in glob.glob(os.path.join(path, '*.gif')):
        print(filename)
        in_gif = Gif.from_file(filename)
        gct = in_gif.global_color_table.entries
        print("Length of GCT",len(gct))
        #print(gct[-1].red, gct[-1].green, gct[-1].blue)
        #print(count_available_storage(in_gif))
        print("Check first index of local colour table")
        blocks = in_gif.blocks
        indexlist = []
        for i in range(len(blocks)):
            if str(blocks[i].block_type) == "BlockType.local_image_descriptor":
                indexlist.append(i)
                print(blocks[i].body.flags)
        #set_local_color_table(in_gif)
        #print("lct",len(blocks[indexlist[1]].body.local_color_table.entries))
        print("number of frames:",len(indexlist))
        print()
    """
    gif = "D:\Monash\FIT3162\GIF collection\hw2.gif"
    in_gif = Gif.from_file(gif)
    blocks = in_gif.blocks
    indexlist = []

    for i in range(len(blocks)):
        if str(blocks[i].block_type) == "BlockType.local_image_descriptor":
            indexlist.append(i)

    for i in range(1,len(indexlist)):
        print(len(blocks[indexlist[i]].body.local_color_table.entries))
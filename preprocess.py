from gif import Gif
from kaitai_gif_write import write_to_file
# File preprocess.py
# Author: Jia Qin Choong
# Usage: Preprocess the GIF before encoding

def checkGCT(inputgif):
    """
    This function checks if the GIF has GCT and if it is of size 256
    Called in count_available_storage
    :param inputgif: GIF object
    :return: GIF object
    """
    flag = inputgif.logical_screen_descriptor.flags
    if (flag & 128) != 0:                               # if there is GCT
        global_table = inputgif.global_color_table
        if len(global_table.entries) == 256:            # if size of GCT is 256
            return inputgif

        else:                                           # if size not 256
            old_table = global_table.entries
            new_table = Gif.ColorTable(global_table._io)        # create new empty table
            for i in range(256):
                if i < len(old_table):              # append the old table RGB values
                    newcolor = Gif.ColorTableEntry(None)
                    newcolor.red = old_table[i].red
                    newcolor.green = old_table[i].green
                    newcolor.blue = old_table[i].blue
                    new_table.entries.append(newcolor)

                else:                                       # create empty RGB values for new entries
                    newcolor = Gif.ColorTableEntry(None)
                    newcolor.red = 0
                    newcolor.green = 0
                    newcolor.blue = 0
                    new_table.entries.append(newcolor)
            inputgif.global_color_table = new_table

        inputgif.logical_screen_descriptor.flags = 247          # change the flag value to indicate correct size of gct
    # else no gct just return inputgif
    return inputgif

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

def get_lct_index(inputgif):
    """
    This function gets the indices of the frames in GIF blocks
    Called in set_local_color_table
    :param inputgif: GIF object
    :return: list of index
    """
    blocks = inputgif.blocks  # the frames are stored in blocks
    indexlist = []
    # get all the indices of frames of a gif
    for i in range(len(blocks)):
        if str(blocks[i].block_type) == "BlockType.local_image_descriptor":
            indexlist.append(i)

    return indexlist

def set_local_color_table(inputgif):
    """
    This function sets the local colour table for each frame if it does not have a local color table
    Called in count_available_storage
    :param inputgif: GIF object
    :return: a list of indices of the local color table
    """
    blocks = inputgif.blocks            # the frames are stored in blocks
    indexlist = get_lct_index(inputgif)

    # the first local colour table should not be changed
    for i in range(1,len(indexlist)):
        index = indexlist[i]
        if blocks[index].body.flags > 0:                     # more than 0 if there is a local color table
            pass

        else:                                                # 0 if there is no local color table
            blocks[index].body.flags = 135                   # set the flag to more than 0 to indicate there is color table
            new_table = copy_global_ct(inputgif)
            inputgif.blocks[index].body.local_color_table = new_table

    return indexlist

def count_available_storage(inputgif):
    """
    A function to count how many characters can be stored in the GIF
    Note:
    Total number of tables = global (1) + local color table (n) - first local color table (1)
    = n
    :param inputgif: The target GIF object
    :return: total number of characters to be stored in the GIF
    """
    count = 0
    inputgif = checkGCT(inputgif)

    if inputgif.logical_screen_descriptor.flags >= 128:        # if there is gct
        count += 1

    frames = len(set_local_color_table(inputgif))- 1                    # number of frames/local color tables available
    count = ((256 * 3) - 8) * (frames + count)                         # total number of bits to be stored in local and global color table
    # first 8 bit used to store the number of characters in the table
    count = count // 8                                      # divide by 8-bit (ASCII) to get character count
    return count

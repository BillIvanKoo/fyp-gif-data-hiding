from gif import Gif

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
    frames = len(set_local_color_table(inputgif))           # number of frames/local color tables available
    count += ((256 * 3) - 8) * frames                       # total number of bits to be stored in local and global color table
    count = count // 8                                      # divide by 8-bit (ASCII) to get character count
    return count

def read_message(filename):
    """
    This function reads a file into a string
    :param filename: file path
    :return: a string containing the contents of the file
    """
    openfile = open(filename, "r")
    message = ""
    for lines in openfile:
        message += lines
    return message

# NEED TO ADD ANOTHER PREPROCESSING TO MAKE SURE GLOBAL COLOR TABLE IS OF SIZE 256

if __name__ == "__main__":
    path = "D:\Monash\FIT3162\GIF collection\shiba.gif"
    in_gif = Gif.from_file(path)
    print(count_available_storage(in_gif))
    print(len(read_message("message.txt")))

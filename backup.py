from gif import Gif
from kaitai_gif_demo import write_to_file
import os
def count_available_storage(inputgif):
    """
    A function to count how many characters can be stored in the GIF
    :param inputgif: The target GIF object
    :return: total number of characters to be stored in the GIF
    """
    # global colour table available storage
    count = 255 * 3
    frames = len(set_local_color_table(inputgif)) - 1     # number of frames available, not including the first frame
    count += 255 * 3 * frames               # total number of bits to be stored
    count = count // 8                      # divide by each 8-bit ASCII to get character count
    return count

def lsb_global(inputgif, message):
    color_table = inputgif.global_color_table.entries
    charlist = [format(ord(c), '08b') for c in message]  # changes the characters to 7-bit ASCII values in BINARY

    print(charlist)
    bitstring = "".join(charlist)

    i = 0
    count = 0
    while i < len(color_table) and count < len(bitstring):
        bit1 = bitstring[count]
        bit2 = bitstring[count + 1]
        bit3 = bitstring[count + 2]
        # bit1 for RED
        if color_table[i].red % 2 != 0:
            # if RED value is odd, LSB is 1
            if bit1 == "0":
                # if the bit is 0, decrement value to make it 0
                color_table[i].red -= 1

                # if the bit is 0, do nothing (maintain the bit)

        elif color_table[i].red % 2 == 0:
            # if RED value is even, LSB is 0
            if bit1 == "1":
                # if the bit is 1, increment value to make it 1
                color_table[i].red += 1

                # if the bit is 1, do nothing (maintain the bit)

        # bit2 for GREEN
        if color_table[i].green % 2 != 0:
            # if GREEN value is odd, LSB is 1
            if bit2 == "0":
                # if the bit is 0, decrement value to make it 0
                color_table[i].green -= 1

        elif color_table[i].green % 2 == 0:
            # if GREEN value is even, LSB is 0
            if bit2 == "1":
                # if bit is 1, increment value to make it 1
                color_table[i].green += 1

        # bit3 for BLUE
        if color_table[i].blue % 2 != 0:
            # if BLUE value is odd, LSB is 1
            if bit3 == "0":
                # if the bit is 0, decrement value to make it 0
                color_table[i].blue -= 1

        elif color_table[i].blue % 2 == 0:
            # if BLUE value is even, LSB is 0
            if bit3 == "1":
                # if bit is 1, increment value to make it 1
                color_table[i].blue += 1

        i += 1
    # include length of the message in the last index??

    # update the GIF object attribute
    inputgif.global_color_table.entries = color_table
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

def set_local_color_table(inputgif):
    blocks = inputgif.blocks
    indexlist = []
    # get all the indices of frames of a gif
    for i in range(len(blocks)):
        if str(blocks[i].block_type) == "BlockType.local_image_descriptor":
            indexlist.append(i)

    # leave the first frame blank without local colour table
    for i in range(1,len(indexlist)):
        index = indexlist[i]
        if blocks[index].body.flags > 0:                     # more than 0 if there is a local color table
            pass

        else:                                               # 0 if there is no local color table
            blocks[index].body.flags = 135                     # set the flag to more than 0 to indicate there is color table
            new_table = copy_global_ct(inputgif)
            inputgif.blocks[index].body.local_color_table = new_table

    return indexlist

if __name__ == "__main__":
    original = Gif.from_file("D:/Monash/FIT3162/GIF collection/levi.gif")
    #encoded = Gif.from_file("D:/Monash/FIT3162/GIF collection/hw-big.gif")

    #in_gif = Gif.from_file("D:\Monash\FIT3162\GIF collection\sns\levi_tumblr.gif")
    #print(lsb_global_decode(in_gif))
    set_local_color_table(original)
    print(count_available_storage(original))
    # get the size of the file in bytes
    size1 = os.path.getsize("D:/Monash/FIT3162/GIF collection/hw.gif")
    size2 = os.path.getsize("D:/Monash/FIT3162/GIF collection/hw-big.gif")
    print(size1)
    print(size2)

from preprocess import *
from encode_gif import lsb_encode
from decode_gif import *
from kaitai_gif_demo import *
import os, glob

def encode(capacity, message, inputgif):
    """
    This function encodes a GIF object and return the encoded GIF object
    :param capacity: int value of max capacity of a GIF
    :param message: string of characters
    :param inputgif: Kaitai object
    :return:
    """
    m_size = len(message)

    # ENCODING PART
    if m_size <= capacity:
        print("Encoding GIF...")
        num_tables = m_size // 95  # number of tables used to store 95 characters

        # first encode in the global color table
        # check is there a gct
        if inputgif.logical_screen_descriptor.flags > 0:
            gct = inputgif.global_color_table.entries
            gct = lsb_encode(message[0:95], gct)
            inputgif.global_color_table.entries = gct           # update the global color table

        # if the tables to be used is more than 1 (there are still message to be encoded)
        if num_tables > 1:
            tables_index = set_local_color_table(in_gif)        # set the local color table if there is no local color table and get index
            blocks = inputgif.blocks
            m_index = 95

            # loop through the local color tables
            for i in range(1, num_tables + 1):  # dont include index 0 (gct), start from 1 up to num_tables (inclusive)
                index = tables_index[i]
                lct = blocks[index].body.local_color_table.entries
                lct = lsb_encode(message[m_index:m_index + 95], lct)    # m_index used to get correct index in the message string
                blocks[index].body.local_color_table.entries = lct      # update lct
                m_index += 95

        print("GIF successfully encoded.")
        return in_gif

    else:
        print("Message size is too large to put in GIF.")
        exit(0)

def decode(inputgif):
    """
    This function decodes a message from the GIF object
    :param inputgif: Kaitai GIF object
    :return: string of characters
    """
    # DECODING PART
    print("Decoding GIF...")
    if inputgif.logical_screen_descriptor.flags > 0:        # if there is a global color table
        gct = inputgif.global_color_table.entries           # get global color table
        result = lsb_decode(gct)

        if len(result) != 95:                               # if the length of message not 95, encoded message is retrieved
            return result                                   # return result

    # otherwise look into local color tables
    blocks = inputgif.blocks
    tables_index = get_lct_index(inputgif)

    for i in range(1, len(tables_index)):
        index = tables_index[i]
        lct = blocks[index].body.local_color_table.entries  # get local color table
        temp = lsb_decode(lct)                              # decode local color table
        result += temp
        if len(temp) != 95:         # break the loop when you first get character count != 95 (this is the remaining characters left)
            break

    return result

if __name__ == "__main__":

    path = "D:/Monash/FIT3162/GIF collection/levi.gif"
    newpath = "D:/Monash/FIT3162/GIF collection/encoded/levi-encoded.gif"
    message = "secret message hi hello annyeong!!"

    in_gif = Gif.from_file(path)
    print(in_gif.logical_screen_descriptor.flags)
    capacity = count_available_storage(in_gif)
    gif = encode(capacity, message, in_gif)
    #write_to_file(gif,newpath)
    print(decode(gif))

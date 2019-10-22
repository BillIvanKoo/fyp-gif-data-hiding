from preprocess import *
from encode_gif import *
from decode_gif import *
from kaitai_gif_demo import *
import os, glob

def encode(path, newpath, messagefile):
    # capacity, message, GIF)
    in_gif = Gif.from_file(path)
    capacity = count_available_storage(in_gif)
    #print("Total available storage in GIF (#characters): ", capacity)

    message = read_message(messagefile)         # read the message file into a string
    m_size = len(message)
    #print("Message size is: ", m_size)

    # ENCODING PART
    if m_size <= capacity:
        print("Encoding GIF...")

        num_tables = m_size // 95  # number of tables used to store 95 characters
        remain = m_size % 95  # remaining characters to be extracted from the last table

        # first encode in the global color table
        gct = in_gif.global_color_table.entries
        gct = lsb_encode(message[0:95], gct)
        # update the global color table
        in_gif.global_color_table.entries = gct

        # if the tables to be used is more than 0 (there are still message to be encoded)
        if num_tables > 0:
            tables_index = set_local_color_table(in_gif)
            blocks = in_gif.blocks
            m_index = 95

            # loop through the local color tables
            for i in range(1, num_tables + 1):  # dont include index 0, start from 1 up to num_tables (inclusive)
                index = tables_index[i]
                lct = blocks[index].body.local_color_table.entries
                lct = lsb_encode(message[m_index:m_index + 95], lct)
                blocks[index].body.local_color_table.entries = lct
                m_index += 95

        write_to_file(in_gif, newpath)
        print("GIF successfully encoded.")

    else:
        print("Message size is too large to put in GIF.")
        exit(0)

def decode(path):
    # DECODING PART
    print("Decoding GIF...")
    encoded = Gif.from_file(path)
    gct = encoded.global_color_table.entries
    result = lsb_decode(gct)

    if len(result) != 95:
        return result

    blocks = encoded.blocks
    tables_index = get_lct_index(encoded)

    for i in range(1, len(tables_index)):
        index = tables_index[i]
        lct = blocks[index].body.local_color_table.entries
        temp = lsb_decode(lct)
        result += temp
        if len(temp) != 95:         # break the loop when you first get character count != 95 (this is the remaining characters left)
            break

    return result
    #file = open("result.txt", "w")
    #file.write(result)
    #file.close()
    #print("GIF successfully decoded. Output is in result.txt")

if __name__ == "__main__":
    """
    path = "D:/Monash/FIT3162/GIF collection/hw2.gif"
    newpath = "D:\Monash\FIT3162\GIF collection\output.gif"
    messagefile = "message.txt"
    encode(path, newpath, messagefile)
    decode(newpath)
    """
    path = "D:/Monash/FIT3162/GIF collection/levi.gif"
    newpath = "D:/Monash/FIT3162/GIF collection/encoded/levi-encoded.gif"
    messagefile = "message.txt"
    #encode(path, newpath, messagefile)

    sns = "D:/Monash/FIT3162/GIF collection/sns/tumblr/c.gif"
    #decode(sns)

    giphy = "D:/Monash/FIT3162/GIF collection/sns/giphy"
    for filename in glob.glob(os.path.join(giphy, '*.gif')):
        #print(filename)
        in_gif = Gif.from_file(filename)
        #print(os.path.getsize(filename))

    new = "D:\Monash\FIT3162\GIF collection\encoded/c-encoded.gif"
    res = decode(new)
    print(res)


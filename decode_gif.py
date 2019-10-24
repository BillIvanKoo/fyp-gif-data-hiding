# File decode_gif.py
# Author: Jia Qin Choong
# Usage: Functions used to decode the message from a color table

def binarytoASCII(bitstring):
    """
    This function changes a bitstring to a normal ASCII string
    :param bitstring: string of 0s and 1s
    :return: string of characters
    """
    # ASCII characters have 8 bits
    res = ""
    for i in range(0,len(bitstring),8):
        binstring = bitstring[i:i+8]
        char = chr(int(binstring,2))
        res += char
    return res

def lsb_decode(color_table):
    """
    This function converts encoded colour table to string of decoded characters
    :param color_table: GIF color table
    :return: string of characters
    """
    bitstring = ""
    for i in range(len(color_table)):
        red = color_table[i].red
        green = color_table[i].green
        blue = color_table[i].blue
        # Append RED LSB first
        if red % 2 == 0:
            bitstring += "0"

        elif red % 2 != 0:
            bitstring += "1"

        # Then GREEN LSB
        if green % 2 == 0:
            bitstring += "0"

        elif green % 2 != 0:
            bitstring += "1"

        # Finally BLUE LSB
        if blue % 2 == 0:
            bitstring += "0"

        elif blue % 2 != 0:
            bitstring += "1"

    length = int(bitstring[0:8],2)
    decoded = binarytoASCII(bitstring[8:(length+1)*8])
    return decoded
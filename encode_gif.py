# File encode_gif.py
# Author: Jia Qin Choong
# Usage: Functions used to encode message into a color table

def lsb_encode(message,color_table):
    """
    This function encodes (part of) message into a color table of a GIF
    :param inputgif: GIF object
    :param message: string of characters (max 95 characters)
    :param color_table: global or local color table
    :return: color table
    """
    # color_table = inputgif.global_color_table.entries
    # get list of characters in 8 bit binary

    # Check if the message size is too big, raise error
    if len(message) > 95:
        raise Exception("Message size is too big for the array!")

    charlist = [format(ord(c),'08b') for c in message]          # changes the characters to 8-bit ASCII values in BINARY
    bitstring = "".join(charlist)                               # join all into a bitstring

    # First 8 bit is the length of the message stored in the table
    first = format(len(message),'08b')
    bitstring = first + bitstring
    remaining = len(bitstring) % 3                              # to deal with remaining bits later

    i = 0
    j = 0
    # while the color table is not full and there are still characters in bitstring
    while i < len(color_table) and j+2 < len(bitstring):
        bit1 = bitstring[j]                     # RED
        bit2 = bitstring[j + 1]                 # GREEN
        bit3 = bitstring[j + 2]                 # BLUE

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
        j += 3
        i += 1
    # i and j now stores the last index accessed by colourtable and bitstring
    last_table_index = i
    last_string_index = j

    # if there are remaining bits
    if remaining == 1:
    # if remaining bit is 1, next bit should be stored in RED
        lastbit = bitstring[last_string_index]

        if color_table[last_table_index].red % 2 != 0:
            if lastbit == "0":
                color_table[last_table_index].red -= 1

        elif color_table[last_table_index].red % 2 == 0:
            if lastbit == "1":
                color_table[last_table_index].red += 1

    elif remaining == 2:
    # if remaining bits are 2, next bits should be stored in RED and GREEN
        last2bit = bitstring[last_string_index]
        lastbit = bitstring[last_string_index + 1]

        # RED
        if color_table[last_table_index].red % 2 != 0:
            if last2bit == "0":
                color_table[last_table_index].red -= 1

        elif color_table[last_table_index].red % 2 == 0:
            if last2bit == "1":
                color_table[last_table_index].red += 1

        # GREEN
        if color_table[last_table_index].green % 2 != 0:
            if lastbit == "0":
                color_table[last_table_index].green -= 1

        elif color_table[last_table_index].green % 2 == 0:
            if lastbit == "1":
                color_table[last_table_index].green += 1

    return color_table
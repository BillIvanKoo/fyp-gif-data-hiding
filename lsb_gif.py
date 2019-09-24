from gif import Gif
from kaitai_gif_demo import write_to_file
def binarytoASCII(bitstring):
    # ASCII characters have 8 bits
    res = ""
    for i in range(0,len(bitstring),8):
        binstring = bitstring[i:i+8]
        char = chr(int(binstring,2))
        res += char
    return res

def lsb_global_encode(inputgif, message):
    color_table = inputgif.global_color_table.entries
    charlist = [format(ord(c),'08b') for c in message]                  # changes the characters to 7-bit ASCII values in BINARY

    bitstring = "".join(charlist)
    remaining = len(bitstring) % 3
    i = 0
    j = 0
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

    # include length of the message in the last index??
    color_table[-1].red = len(bitstring)

    # update the GIF object attribute
    inputgif.global_color_table.entries = color_table
    return inputgif

def lsb_global_decode(encodedgif):
    decoded = ""
    bitstring = ""
    color_table = encodedgif.global_color_table.entries
    # the length of the message (in bits) is  stored in the last global table
    length = color_table[-1].red
    remaining = length % 3

    for i in range(length//3):
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

    last_index = length//3

    if remaining == 1:
        # Get LSB from RED
        if color_table[last_index].red % 2 == 0:
            bitstring += "0"

        elif color_table[last_index].red % 2 != 0:
            bitstring += "1"

    if remaining == 2:
        # Get LSB from RED and GREEN
        if color_table[last_index].red % 2 == 0:
            bitstring += "0"

        elif color_table[last_index].red % 2 != 0:
            bitstring += "1"

        if color_table[last_index].green % 2 == 0:
            bitstring += "0"

        elif color_table[last_index].green % 2 != 0:
            bitstring += "1"

    decoded = binarytoASCII(bitstring)
    return decoded
if __name__ == "__main__":
    in_gif = Gif.from_file("D:\Monash\FIT3162\GIF collection\levi.gif")
    message = "!@#$%^&*()"
    #opfile = open("message.txt")
    #message = opfile.readline()
    #print(len(message))
    out_gif = lsb_global_encode(in_gif,message)
    print("Bits encoded:", in_gif.global_color_table.entries[-1].red)

    #print("GENERATING GIF...")
    #write_to_file(out_gif,"D:\Monash\FIT3162\GIF collection\levi_encoded.gif")
    #print("GIF GENERATED")

    print("DECODING GIF...")
    decoded = lsb_global_decode(out_gif)
    print("Decoded message:",decoded)

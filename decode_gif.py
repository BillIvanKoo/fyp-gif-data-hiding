from gif import Gif
from encode_gif import lsb_encode

def binarytoASCII(bitstring):
    # ASCII characters have 8 bits
    res = ""
    for i in range(0,len(bitstring),8):
        binstring = bitstring[i:i+8]
        char = chr(int(binstring,2))
        res += char
    return res

def lsb_decode(color_table):
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
    print(length)
    # check if the length is less than 95, if not then there is no data hidden, return empty string
    if length > 95:
        decoded = ""
    else:
        decoded = binarytoASCII(bitstring[8:(length+1)*8])

    return decoded

if __name__ == "__main__":
    path = "D:\Monash\FIT3162\GIF collection\shiba.gif"
    in_gif = Gif.from_file(path)
    color_table = in_gif.global_color_table.entries
    msg = "secretmessage???"
    print("length",len(msg))
    color_table = lsb_encode(msg,color_table)
    print("Encode success!")
    lsb_decode(color_table)
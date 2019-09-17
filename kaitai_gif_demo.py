from gif import Gif
def compareGIFs(gif1,gif2):
    """
    This function compares 2 gifs' global colour table entries to see if they are similar
    :param gif1: original gif
    :param gif2: downloaded gif
    :return: true or false
    """
    color_table1 = gif1.global_color_table.entries
    color_table2 = gif2.global_color_table.entries
    count = 0
    for i in range(len(color_table1)):
        color1 = color_table1[i]
        color2 = color_table2[i]
        # color3 = color_table3[i]

        if color1.red == color2.red and color1.green == color2.green and color1.blue == color2.blue:
            count += 1
        else:
            pass
    print(count)
    if count == 256:
        return True
    else:
        return False

def countEmptyPixels(input):
    """
    Get the empty pixels index in a GIF
    where the pixel has RGB value (0,0,0)
    :param input: input is the GIF kaitai object
    :return: a list of indices which has no rgb values
    """
    color_table = input.global_color_table.entries
    indexlist = []
    for i in range(256):
        rgb = color_table[i]
        if (rgb.red == 0 and rgb.blue == 0 and rgb.green == 0):
            indexlist.append(i)

    return indexlist

data1 = Gif.from_file("D:\Monash\FIT3162\GIF collection\levi.gif")
#data2 = Gif.from_file("D:\Monash\FIT3162\GIF collection\levi-tumblr.gif")
data2 = Gif.from_file("D:\Monash\FIT3162\GIF collection\levi2.gif")

# local screen descriptor
#print(data1.logical_screen_descriptor.screen_width)
#print(data2.logical_screen_descriptor.screen_width)
#print(data3.logical_screen_descriptor.screen_width)

color_table1 = data1.global_color_table.entries
#color_table2 = data2.global_color_table.entries
#color_table3 = data3.global_color_table.entries

first_color1 = color_table1[0]
#first_color2 = color_table2[0]
#first_color3 = color_table3[0]

print(first_color1.red, first_color1.green, first_color1.blue)
#print(first_color2.red, first_color2.green, first_color2.blue)
#print(first_color3.red, first_color3.green, first_color3.blue)

blocks1 = data1.blocks
blocks2 = data2.blocks
#blocks3 = data3.blocks

#for i in range(len(blocks1)):
#    print(blocks1[i].block_type)

print(compareGIFs(data1,data2))

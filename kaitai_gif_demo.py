from gif import Gif

data1 = Gif.from_file("../../../Downloads/safe_image.gif")
data2 = Gif.from_file("../../../Downloads/tumblr_pvk36wTOsT1ytp1fjo1_540.gif")
print(data1.hdr.version)

color_table1 = data1.global_color_table.entries
color_table2 = data2.global_color_table.entries

first_color1 = color_table1[0]
first_color2 = color_table2[0]

print(first_color1.red, first_color1.green, first_color1.blue)
print(first_color2.red, first_color2.green, first_color2.blue)

blocks1 = data1.blocks

for i in blocks1:
    if i.block_type == BlockType
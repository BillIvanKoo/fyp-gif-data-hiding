from gif import Gif

def write_to_file(gif, filename):
    assert isinstance(gif, Gif)
    """

    :param filename: file name to write the GIF object to
    :return: None
    :author: Bill Ivan Kooslarto
    """
    res = bytearray(gif.hdr.magic)
    res += bytearray(gif.hdr.version, "ascii")
    lsd = gif.logical_screen_descriptor
    res += bytearray(lsd.screen_width.to_bytes(2, 'little'))
    res += bytearray(lsd.screen_height.to_bytes(2, 'little'))
    res += bytearray(lsd.flags.to_bytes(1, 'little'))
    res += bytearray(lsd.bg_color_index.to_bytes(1, 'little'))
    res += bytearray(lsd.pixel_aspect_ratio.to_bytes(1, 'little'))
    if lsd.has_color_table:
        for i in gif.global_color_table.entries:
            res += bytearray(i.red.to_bytes(1, 'little'))
            res += bytearray(i.green.to_bytes(1, 'little'))
            res += bytearray(i.blue.to_bytes(1, 'little'))
    for i in gif.blocks:
        res += bytearray(i.block_type.value.to_bytes(1, 'little'))
        if i.block_type == Gif.BlockType.extension:
            res += bytearray(i.body.label.value.to_bytes(1, 'little'))
            if i.body.label == Gif.ExtensionLabel.graphic_control:
                gc_body = i.body.body
                res += bytearray(gc_body.block_size)
                res += bytearray(gc_body.flags.to_bytes(1, 'little'))
                res += bytearray(gc_body.delay_time.to_bytes(2, 'little'))
                res += bytearray(gc_body.transparent_idx.to_bytes(1, 'little'))
                res += bytearray(gc_body.terminator)
            elif i.body.label == Gif.ExtensionLabel.comment:
                print("comment")
            elif i.body.label == Gif.ExtensionLabel.application:
                app_body = i.body.body
                res += bytearray(app_body.application_id.num_bytes.to_bytes(1, 'little'))
                res += bytearray(app_body.application_id.bytes)
                for j in app_body.subblocks:
                    res += bytearray(j.num_bytes.to_bytes(1, 'little'))
                    res += bytearray(j.bytes)
                    # print(j.num_bytes, j.bytes)
            else:
                print('Plain text')
        if i.block_type == Gif.BlockType.local_image_descriptor:
            res += bytearray(i.body.left.to_bytes(2, 'little'))
            res += bytearray(i.body.top.to_bytes(2, 'little'))
            res += bytearray(i.body.width.to_bytes(2, 'little'))
            res += bytearray(i.body.height.to_bytes(2, 'little'))
            res += bytearray(i.body.flags.to_bytes(1, 'little'))
            if i.body.has_color_table:
                for c in i.body.local_color_table.entries:
                    res += bytearray(c.red.to_bytes(1, 'little'))
                    res += bytearray(c.green.to_bytes(1, 'little'))
                    res += bytearray(c.blue.to_bytes(1, 'little'))
            res += bytearray(i.body.image_data.lzw_min_code_size.to_bytes(1, 'little'))
            for j in i.body.image_data.subblocks.entries:
                res += bytearray(j.num_bytes.to_bytes(1, 'little'))
                res += bytearray(j.bytes)
    with open(filename, 'wb+') as f:
        f.write(res)

    print(len(res))

def decode_lzw(imageData):
    assert isinstance(imageData, Gif.ImageData)
    EOI = "EOI"
    CC = "Clear"
    bits_to_decode = imageData.lzw_min_code_size + 1
    lzw_table_size = (2 ** imageData.lzw_min_code_size) + 2
    lzw_table = [[str(i)] for i in range(lzw_table_size)]
    lzw_table[-1] = [EOI]
    lzw_table[-2] = [CC]
    indexstream = []

    bit_str = ""
    for i in imageData.subblocks.entries:

        bit_str = bin(int.from_bytes(i.bytes, byteorder='little'))[2:].zfill(i.num_bytes*8) + bit_str

    # remove clear code
    bit_str = bit_str[:-bits_to_decode]

    # start with first item
    curr_code = int(bit_str[-bits_to_decode:], 2)
    bit_str = bit_str[:-bits_to_decode]
    indexstream += lzw_table[curr_code]
    prev_code = curr_code

    count = 1
    while True:
        curr_code = int(bit_str[-bits_to_decode:], 2)
        bit_str = bit_str[:-bits_to_decode]
        if curr_code < len(lzw_table):
            if lzw_table[curr_code] == [EOI]:
                print("END HERE", count)
                break
            if lzw_table[curr_code] == [CC]:
                print("CLEAR HERE", count)
                lzw_table = [[str(i)] for i in range(lzw_table_size)]
                lzw_table[-1] = [EOI]
                lzw_table[-2] = [CC]
                bits_to_decode = imageData.lzw_min_code_size + 1
                curr_code = int(bit_str[-bits_to_decode:], 2)
                bit_str = bit_str[:-bits_to_decode]
                prev_code = None
                print(curr_code)
            indexstream += lzw_table[curr_code]
            if prev_code is not None:
                K = lzw_table[curr_code][0]
                new_entry = lzw_table[prev_code][:]

                new_entry.append(K)
                lzw_table.append(new_entry)
        else:
            try:
                K = lzw_table[prev_code][0]
            except IndexError as e:
                print(prev_code)
                print(len(lzw_table))
            new_entry = lzw_table[prev_code][:]
            new_entry.append(K)
            indexstream += new_entry
            lzw_table.append(new_entry)
        prev_code = curr_code

        if len(lzw_table) == (2 ** bits_to_decode):
            print(len(lzw_table))
            if bits_to_decode < 12:
                bits_to_decode += 1
        if len(bit_str) < bits_to_decode:
            print(bit_str)
            print(len(lzw_table))
            break
        count += 1

    return indexstream



if __name__ == "__main__":
    # data1 = Gif.from_file("../../../Downloads/parrot.gif")
    # data1 = Gif.from_file("../../../Downloads/sample_1.gif")
    data1 = Gif.from_file("../../../Downloads/Earth-29-june.gif")
    # data2 = Gif.from_file("../../../Downloads/tumblr_pvk36wTOsT1ytp1fjo1_540.gif")
    # print(data1.hdr.magic)
    print(data1.hdr.version)


    # color_table1 = data1.global_color_table.entries
    # color_table2 = data2.global_color_table.entries

    # for i in range(1, len(color_table1)):
    #     color1 = color_table1[i]
    #     color2 = color_table2[i]
    #
    #     print(i, "\t", color1.red, color1.green, color1.blue, "\t", color2.red, color2.green, color2.blue)

    # print(data2.logical_screen_descriptor.has_color_table)
    # print(data2.logical_screen_descriptor.flags)
    # data2.logical_screen_descriptor.flags ^= 128
    # print(data2.logical_screen_descriptor.has_color_table)
    # print(data2.logical_screen_descriptor.flags)
    blocks1 = data1.blocks
    for i in blocks1:
        if i.block_type == Gif.BlockType.local_image_descriptor:
            decode_lzw(i.body.image_data)

    # blocks2 = data2.blocks
    # print(len(blocks1))
    # print(len(blocks2))
    # write_to_file(data2, "result.gif");

    # for i in range(len(blocks1)):
    #     if i >= len(blocks2):
    #         print(i, blocks1[i].block_type)
    #     else:
    #         print(i, "\t", blocks1[i].block_type, "\t", blocks2[i].block_type)
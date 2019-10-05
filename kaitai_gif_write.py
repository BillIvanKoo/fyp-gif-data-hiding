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
                for j in i.body.body.entries:
                    res += bytearray(j.num_bytes.to_bytes(1, 'little'))
                    res += bytearray(j.bytes)
            elif i.body.label == Gif.ExtensionLabel.application:
                app_body = i.body.body
                res += bytearray(app_body.application_id.num_bytes.to_bytes(1, 'little'))
                res += bytearray(app_body.application_id.bytes)
                for j in app_body.subblocks:
                    res += bytearray(j.num_bytes.to_bytes(1, 'little'))
                    res += bytearray(j.bytes)
            else:
                for j in i.body.body.entries:
                    res += bytearray(j.num_bytes.to_bytes(1, 'little'))
                    res += bytearray(j.bytes)
        if i.block_type == Gif.BlockType.local_image_descriptor:
            res += bytearray(i.body.left.to_bytes(2, 'little'))
            res += bytearray(i.body.top.to_bytes(2, 'little'))
            res += bytearray(i.body.width.to_bytes(2, 'little'))
            res += bytearray(i.body.height.to_bytes(2, 'little'))
            res += bytearray(i.body.flags.to_bytes(1, 'little'))
            if (i.body.flags & 128) != 0:
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

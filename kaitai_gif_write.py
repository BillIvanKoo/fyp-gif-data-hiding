"""
Filename: kaitai_gif_write.py
Author:  Bill Ivan Kooslarto - 28694120
Writing implementation of Kaitai Gif object,
by turning the object to bytearray
"""
from gif import Gif
import copy
import math

def gif_to_bytearray(gif):
    """
    Turn Kaitai Gif object to bytearray
    :param gif: the Kaitai Gif object to turn to bytearray
    :return: The bytearray of the gif 
    :author: Bill Ivan Kooslarto - 28694120
    """
    assert isinstance(gif, Gif)

    # header
    res = bytearray(gif.hdr.magic)
    res += bytearray(gif.hdr.version, "ascii")
    
    # logical screen descriptor
    lsd = gif.logical_screen_descriptor
    res += bytearray(lsd.screen_width.to_bytes(2, 'little'))
    res += bytearray(lsd.screen_height.to_bytes(2, 'little'))
    res += bytearray(lsd.flags.to_bytes(1, 'little'))
    res += bytearray(lsd.bg_color_index.to_bytes(1, 'little'))
    res += bytearray(lsd.pixel_aspect_ratio.to_bytes(1, 'little'))
    
    # global color table
    if lsd.has_color_table:
        for i in gif.global_color_table.entries:
            res += bytearray(i.red.to_bytes(1, 'little'))
            res += bytearray(i.green.to_bytes(1, 'little'))
            res += bytearray(i.blue.to_bytes(1, 'little'))
    
    # remaining blocks
    for i in gif.blocks:
        # block type
        res += bytearray(i.block_type.value.to_bytes(1, 'little'))
        
        # if extension
        if i.block_type == Gif.BlockType.extension:
            res += bytearray(i.body.label.value.to_bytes(1, 'little'))
            # if graphic control
            if i.body.label == Gif.ExtensionLabel.graphic_control:
                gc_body = i.body.body
                res += bytearray(gc_body.block_size)
                res += bytearray(gc_body.flags.to_bytes(1, 'little'))
                res += bytearray(gc_body.delay_time.to_bytes(2, 'little'))
                res += bytearray(gc_body.transparent_idx.to_bytes(1, 'little'))
                res += bytearray(gc_body.terminator)
            # elif application
            elif i.body.label == Gif.ExtensionLabel.application:
                app_body = i.body.body
                res += bytearray(app_body.application_id.num_bytes.to_bytes(1, 'little'))
                res += bytearray(app_body.application_id.bytes)
                for j in app_body.subblocks:
                    res += bytearray(j.num_bytes.to_bytes(1, 'little'))
                    res += bytearray(j.bytes)
            # comment or plain text
            else:
                for j in i.body.body.entries:
                    res += bytearray(j.num_bytes.to_bytes(1, 'little'))
                    res += bytearray(j.bytes)
        
        # local image descriptor
        if i.block_type == Gif.BlockType.local_image_descriptor:
            res += bytearray(i.body.left.to_bytes(2, 'little'))
            res += bytearray(i.body.top.to_bytes(2, 'little'))
            res += bytearray(i.body.width.to_bytes(2, 'little'))
            res += bytearray(i.body.height.to_bytes(2, 'little'))
            res += bytearray(i.body.flags.to_bytes(1, 'little'))
            # check for local color table
            if (i.body.flags & 128) != 0:
                for c in i.body.local_color_table.entries:
                    res += bytearray(c.red.to_bytes(1, 'little'))
                    res += bytearray(c.green.to_bytes(1, 'little'))
                    res += bytearray(c.blue.to_bytes(1, 'little'))
            res += bytearray(i.body.image_data.lzw_min_code_size.to_bytes(1, 'little'))
            for j in i.body.image_data.subblocks.entries:
                res += bytearray(j.num_bytes.to_bytes(1, 'little'))
                res += bytearray(j.bytes)
    return res

def write_to_file(gif, filename):
    """
    turn Kaitai Gif object to bytearray then write it into a file
    :param filename: file name to write the GIF object to
    :param gif: the Kaitai Gif object to write to a file
    :return: None
    :author: Bill Ivan Kooslarto - 28694120
    """
    res = gif_to_bytearray(gif)
    with open(filename, 'wb+') as f:
        f.write(res)


"""
File name: image_data-lzw.py
Author: Bill Ivan Kooslarto - 28694120
Module to LZW decompress and compress image data in Kaitai GIF Object
"""
from gif import Gif
import math

EOI = "EOI"
CC = "Clear"


def decode(image_data):
    """
    LZW Decompression for Kaitai GIF image data
    @author: Bill Ivan Kooslarto - 28694120
    @param image_data: a Kaitai Gif.ImageData object
    @return: array of indexes
    """
    assert isinstance(image_data, Gif.ImageData)
    
    # initialise the LZW table
    bits_to_decode = image_data.lzw_min_code_size + 1
    lzw_table_size = (2 ** image_data.lzw_min_code_size) + 2
    lzw_table = [[str(i)] for i in range(lzw_table_size)]
    lzw_table[-1] = [EOI]
    lzw_table[-2] = [CC]
    index_stream = []

    # serialise the data in the subblocks into string
    bit_str = ""
    for i in image_data.subblocks.entries:
        if i.bytes != b'':
            bit_str = bin(int.from_bytes(i.bytes, byteorder='little'))[2:].zfill(i.num_bytes*8) + bit_str

    # remove clear code
    bit_str = bit_str[:-bits_to_decode]
    
    # LZW decompression starts
    # start with first item
    curr_code = int(bit_str[-bits_to_decode:], 2)
    bit_str = bit_str[:-bits_to_decode]
    index_stream += lzw_table[curr_code]
    prev_code = curr_code

    count = 1
    while True:
        curr_code = int(bit_str[-bits_to_decode:], 2)
        bit_str = bit_str[:-bits_to_decode]
        if curr_code < len(lzw_table):
            # if it is the end of the image break out of the loop
            if lzw_table[curr_code] == [EOI]:
                break
            # if clear code, reset lzw table
            if lzw_table[curr_code] == [CC]:
                lzw_table = [[str(i)] for i in range(lzw_table_size)]
                lzw_table[-1] = [EOI]
                lzw_table[-2] = [CC]
                bits_to_decode = image_data.lzw_min_code_size + 1
                curr_code = int(bit_str[-bits_to_decode:], 2)
                bit_str = bit_str[:-bits_to_decode]
                prev_code = None
            index_stream += lzw_table[curr_code]
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
            index_stream += new_entry
            lzw_table.append(new_entry)
        prev_code = curr_code

        if len(lzw_table) == (2 ** bits_to_decode):
            if bits_to_decode < 12:
                bits_to_decode += 1
        if len(bit_str) < bits_to_decode:
            break
        count += 1

    return index_stream


def encode(index_stream):
    """
    LZW Decompression for Kaitai GIF image data
    @author: Bill Ivan Kooslarto - 28694120
    @param image_data: a Kaitai Gif.ImageData object
    @return: array of indexes
    """
    # initialise LZW table
    max_index = max([int(i, base=10) for i in index_stream])
    min_code = math.ceil(math.log(max_index, 2))
    if min_code == 1:
        min_code = 2
    lzw_table_size = (2 ** min_code) + 2
    lzw_table = [[str(i)] for i in range(lzw_table_size)]
    lzw_table[-1] = [EOI]
    lzw_table[-2] = [CC]

    bits_to_decode = min_code + 1
    code_stream = bin(lzw_table.index([CC]))[2:]
    index_buffer = [index_stream[0][:]]

    # LZW compress the index array to code stream
    for i in range(1, len(index_stream)):
        K = [index_stream[i][:]]
        try:
            lzw_table.index(index_buffer + K)
            index_buffer += K
            if i == len(index_stream) - 1:
                code_stream = bin(lzw_table.index(index_buffer))[2:].zfill(bits_to_decode) + code_stream
        except ValueError:
            lzw_table.append(index_buffer + K)
            code_stream = bin(lzw_table.index(index_buffer))[2:].zfill(bits_to_decode) + code_stream
            index_buffer = K
            if len(lzw_table) > 2 ** bits_to_decode:
                bits_to_decode += 1

    # add end of information code
    code_stream = bin(lzw_table.index([EOI]))[2:] + code_stream

    
    # split the code stream into subblocks
    code_len = len(code_stream)
    i = code_len
    bytes_list = []
    while i >= 0:
        if i < 8:
            byte_string = ("0"*(8-i)) + code_stream[:i]
        else:
            byte_string = code_stream[i-8:i]
        bytes_list = [int(byte_string, 2).to_bytes(len(byte_string)//8, byteorder='little')] + bytes_list
        i -= 8

    max_subblock_len = 255
    new_entries = []
    temp_byte = bytearray()
    byte_count = 0
    for i in range(len(bytes_list)):
        temp_byte = bytes_list[i] + temp_byte
        byte_count += 1
        if byte_count == max_subblock_len or i == len(bytes_list) - 1:
            new_subblock = Gif.Subblock(None)
            new_subblock.num_bytes = byte_count
            new_subblock.bytes = temp_byte
            new_entries.append(new_subblock)
            byte_count = 0

    new_subblock = Gif.Subblock(None)
    new_subblock.num_bytes = 0
    new_subblock.bytes = b''
    new_entries.append(new_subblock)

    return new_entries

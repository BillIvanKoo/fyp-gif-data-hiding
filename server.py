from preprocess import *
from encode_gif import *
from decode_gif import *
from kaitai_gif_demo import *
from kaitaistruct import KaitaiStream, BytesIO
from gif import Gif
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/gif/calculate", methods=['POST'])
def calculate():
    file = request.files['file']
    data = Gif(KaitaiStream(BytesIO(file.read())))
    capacity = count_available_storage(data)
    return {"capacity": capacity}

@app.route("/gif/encode", methods=['POST'])
def encode():
    file = request.files['file']
    in_gif = Gif(KaitaiStream(BytesIO(file.read())))
    message = request.form["message"]
    
    m_size = len(message)
    print("Encoding GIF...")

    num_tables = m_size // 95  # number of tables used to store 95 characters
    remain = m_size % 95  # remaining characters to be extracted from the last table

    # first encode in the global color table
    gct = in_gif.global_color_table.entries
    gct = lsb_encode(message[0:95], gct)
    # update the global color table
    in_gif.global_color_table.entries = gct
    
    # if the tables to be used is more than 0 (there are still message to be encoded)
    if num_tables > 0:
        tables_index = set_local_color_table(in_gif)
        blocks = in_gif.blocks
        m_index = 95

        # loop through the local color tables
        for i in range(1, num_tables + 1):  # dont include index 0, start from 1 up to num_tables (inclusive)
            index = tables_index[i]
            lct = blocks[index].body.local_color_table.entries
            lct = lsb_encode(message[m_index:m_index + 95], lct)
            blocks[index].body.local_color_table.entries = lct
            m_index += 95
    
    gif = in_gif
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
                for j in i.body.entries:
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

    return send_file(BytesIO(bytes(res)), mimetype='image/gif', as_attachment=True, attachment_filename="%s_encoded.gif" % file.filename)

@app.route("/gif/decode", methods=["POST"])
def decode():
    file = request.files['file']
    encoded = Gif(KaitaiStream(BytesIO(file.read())))
    gct = encoded.global_color_table.entries
    result = lsb_decode(gct)

    blocks = encoded.blocks
    tables_index = get_lct_index(encoded)

    for i in range(1, len(tables_index)):
        index = tables_index[i]
        lct = blocks[index].body.local_color_table.entries
        temp = lsb_decode(lct)
        result += temp
        if len(temp) != 95:         # break the loop when you first get character count != 95 (this is the remaining characters left)
            break

    return {"message": result}
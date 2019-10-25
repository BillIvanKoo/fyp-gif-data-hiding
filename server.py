from preprocess import *
from lsb_gif import *
from kaitai_gif_write import gif_to_bytearray
from kaitaistruct import KaitaiStream, BytesIO
from gif import Gif
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
import io

app = Flask(__name__)
CORS(app)

@app.route("/gif/calculate", methods=['POST'])
def calculate_route():
    file = request.files['file']
    data = Gif(KaitaiStream(BytesIO(file.read())))
    capacity = count_available_storage(data)
    return {"capacity": capacity}

@app.route("/gif/encode", methods=['POST'])
def encode_route():
    file = request.files['file']
    gif = Gif(KaitaiStream(BytesIO(file.read())))
    message = request.form["message"]
    
    gif = encode(count_available_storage(gif), message, gif)
    res = gif_to_bytearray(gif)

    return send_file(io.BytesIO(bytes(res)), mimetype='image/gif'); 

@app.route("/gif/decode", methods=["POST"])
def decode_route():
    file = request.files['file']
    encoded = Gif(KaitaiStream(BytesIO(file.read())))
    
    res = decode(encoded)

    return {"message": res}
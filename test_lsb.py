import os, glob, time
from lsb_gif import *
# Author : Jia Qin Choong
# Usage: Testing functions of lsb_gif.py (main functionality)
# Goes through a list of GIFs, encode and decode, check if the message decoded is the same
# Try with different length of message

def test_encode_decode(path, msg):
    cap = len(msg)
    test_count = 0
    gif_count = 0
    for filename in glob.glob(os.path.join(path, '*.gif')):
        gif_count += 1
        inputgif = Gif.from_file(filename)
        encode(cap, msg, inputgif)
        decoded = decode(inputgif)

        if decoded == msg:
            test_count += 1
        else:
            print(filename)
            print(decoded)

    if test_count == gif_count:
        print("Passed all the test.")

if __name__ == '__main__':
    path = "D:\Monash\FIT3162\GIF collection"

    start = time.time()
    msg1 = "This is test message number 3!"
    test_encode_decode(path,msg1)
    end = time.time()
    print("Message length:",len(msg1),"Time taken:", end-start)

    start = time.time()
    msg2 = "123This is a longer message,This is a longer message!This is a longer messageThis is a longer messageThis is a longer message"
    test_encode_decode(path,msg2)
    end = time.time()
    print("Message length:",len(msg2),"Time taken:", end-start)

    start = time.time()
    msg3 = "123This is a longer message,This is a longer message!This is  aaa longer messageThis is a longer messageThis is a longer messageThis is a longer messageThis is a longer messageThis is a longer messageThis is a longer messageThis is a longer message"
    test_encode_decode(path,msg3)
    end = time.time()
    print("Message length:",len(msg3),"Time taken:", end-start)


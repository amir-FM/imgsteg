#!/bin/python3

import sys
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import random

def print_options():
    global image_file
    global data_file
    global mode
    global output_file
    global bits

    print(f"{mode} - {image_file} - {data_file} - {output_file} - {bits}")

def options(index):
    global mode
    global output_file
    global bits

    try:
        if sys.argv[index] == "-o":
            output_file = sys.argv[index + 1]
            return index + 2
        elif sys.argv[index] == "-l":
            bits = int(sys.argv[index + 1])
            return index + 2
        elif sys.argv[index] == "-d":
            mode = "decode"
            return index + 1
        else:
            raise Exception("invalid option")
    except:
        raise Exception("invalid syntax")

def arg_parser():
    #if len(sys.argv) < 3:
    #    raise Exception("Invalid number of arguments")

    global image_file
    global data_file

    image_file = sys.argv[1]
    data_file = sys.argv[2]

    index = 3

    while index < len(sys.argv):
        index = options(index)

def encode(v, s, bits):
    if len(s) * 8 > len(v) * bits:
        raise ValueError("Not enough bits in vector to hide message")

    if len(v) * bits - len(s) * 8 > 16:
        s.extend([ord(x) for x in "END"])

    print(f"bits in image {len(v) * bits}")
    new_v = np.array([], dtype='uint8')
    mask = (0b11111111 << bits) % 256
    char_mask = 2 ** bits - 1
    s_list = list(s)
    total_bits = len(s) * 8
    curr_char = s_list.pop(0)
    print(f"total_bits is {total_bits} and curr char is {curr_char}")
    index = 0

    for elem in v:
        if total_bits == 0:
            break

        elem = (elem & mask) + (curr_char & char_mask)
        new_v = np.append(new_v, elem)
        curr_char >>= bits
        total_bits -= bits
        index += 1

        if total_bits % 8 == 0 and total_bits != 0:
            curr_char = s_list.pop(0)

    print(f"index stopped at {index}")
    new_v = np.append(new_v, v[index:])
    return new_v

def decode(v, bits):
    s = np.array([], dtype='uint8')
    total_bits = len(v) * bits
    total_bits = total_bits - total_bits % 8
    curr_char = 0
    end = 0
    bit_mask = 2 ** bits - 1
    print(f"total_bits is {total_bits}")

    carridge = 0
    for elem in v:
        if total_bits == 0:
            break

        bit = elem & bit_mask
        curr_char = curr_char + (bit << carridge)
        carridge += bits
        total_bits -= bits

        if carridge >= 8:
            carridge = 0
            s = np.append(s, curr_char)
            if chr(curr_char) == 'E':
                end = 1
            elif chr(curr_char) == 'N' and end == 1:
                end = 1
            elif chr(curr_char) == 'D' and end == 1:
                s = s[:-3]
                break
            else:
                end = 0

            curr_char = 0

    return s

mode = "encode"
output_file = "out"
bits = 1
arg_parser()

img = Image.open(image_file)
arr = np.asarray(img)
v = np.ravel(arr)


#print(type(arr))
#print(arr.shape)
#
#v = np.ravel(arr)
#print(v.shape)

if mode == "encode":
    file = open(data_file, "rb")
    data = list(file.read())

    new_v = encode(v, data, bits)
    new_arr = new_v.reshape(arr.shape)
    new_img = Image.fromarray(new_arr)
    new_img.save(output_file)
elif mode == "decode":
    decode(v, bits).tofile(output_file)

#new_v = encode(v, data, bits)
#print(new_v.shape)
#
#new_arr = new_v.reshape(arr.shape)
#print(new_arr.shape)
#print(arr.dtype)
#print(v.dtype)
#print(new_v.dtype)
#print(new_arr.dtype)

#plt.imshow(new_arr, interpolation='nearest')
#plt.show()

#decode(new_v, bits).tofile(output_file)
#
#new_img = Image.fromarray(new_arr)
#new_img.save("new_portal.jpg")

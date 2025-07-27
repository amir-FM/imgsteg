#!/bin/python3

from threading import Thread
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
    global threads

    try:
        if sys.argv[index] == "-o":
            output_file = sys.argv[index + 1]
            return index + 2
        elif sys.argv[index] == "-l":
            bits = int(sys.argv[index + 1])
            return index + 2
        elif sys.argv[index] == "-t":
            threads = int(sys.argv[index + 1])
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

def thread_controller(v, s, bits, threads):
    data_length = list(len(s).to_bytes(8))
    s = data_length + s

    if len(s) * 8 > len(v) * bits:
        raise ValueError("Not enough bits in vector to hide message")

    print(f"bits in image {len(v) * bits} with len {len(v)}")
    print(f"bits in data  {len(s) * 8} with len {len(s)}")
    data_section = len(s) // threads
    image_section = data_section * 8 // bits

    data_index = 0
    image_index = 0

    new_v = np.array([], dtype='uint8')
    thread_v = [[] for i in range(threads)]
    print(f"thread_v len is {thread_v}")

    thrs = []
    for i in range(threads):
        print(f"i este {i}")
        if data_index + 2 * data_section > len(s):
            print(f"data [{data_index}, {len(s) - 1}] and image [{image_index}, {image_index + (len(s) - data_index) * 8 // bits - 1}]")
            t = Thread(target=thread_encode, args=(v[image_index : image_index + (len(s) - data_index) * 8 // bits], s[data_index : len(s)], bits, thread_v[i]))
            thrs.append(t)
            t.start()
        else:
            print(f"data [{data_index}, {data_index + data_section - 1}] and image [{image_index}, {image_index + image_section - 1}]")
            t = Thread(target=thread_encode, args=(v[image_index : image_index + image_section], s[data_index : data_index + data_section], bits, thread_v[i]))
            thrs.append(t)
            t.start()


        data_index += data_section
        image_index += image_section

    for t in thrs:
        t.join()

    for i in range(threads):
        new_v = np.append(new_v, thread_v[i])

    image_index = len(s) * 8 // bits
    print(f"index stopped at {image_index}")
    new_v = np.append(new_v, v[image_index:])
    return new_v

def thread_encode(v, s, bits, new_v):
    print(f"image len {len(v)} and data {len(s)}")
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
        new_v.append(elem)
        curr_char >>= bits
        total_bits -= bits
        index += 1

        if total_bits % 8 == 0 and total_bits != 0:
            curr_char = s_list.pop(0)

def encode(v, s, bits):
    if len(s) * 8 > len(v) * bits:
        raise ValueError("Not enough bits in vector to hide message")

    if len(v) * bits - len(s) * 8 > 16:
        s.extend([ord(x) for x in "END"])

    print(f"bits in image {len(v) * bits} and message {s}")
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
    data_length_bytes = []
    data_length = 0
    length_set = False
    s = np.array([], dtype='uint8')
    total_bits = len(v) * bits
    total_bits = total_bits - total_bits % 8
    curr_char = 0
    bit_mask = 2 ** bits - 1
    print(f"total_bits is {total_bits}")

    carridge = 0
    for elem in v:
        if length_set == True and data_length <= 0:
            break

        bit = elem & bit_mask
        curr_char = curr_char + (bit << carridge)
        carridge += bits
        total_bits -= bits

        if carridge >= 8:
            carridge = 0
            if length_set == False:
                data_length_bytes.append(curr_char)
                if len(data_length_bytes) == 8:
                    data_length = calculate_data_length(data_length_bytes)
                    length_set = True
                    print(f"data_length este {data_length}")
            else:
                s = np.append(s, curr_char)
                data_length -= 1


            curr_char = 0

    return s

def calculate_data_length(bytes_vector):
    return int.from_bytes(bytes(bytes_vector))

mode = "encode"
output_file = "out"
bits = 1
threads = 1
arg_parser()

img = Image.open(image_file)
arr = np.asarray(img)
v = np.ravel(arr)

if mode == "encode":
    file = open(data_file, "rb")
    data = list(file.read())

    new_v = thread_controller(v, data, bits, threads)
    new_arr = new_v.reshape(arr.shape)
    new_img = Image.fromarray(new_arr)
    new_img.save(output_file)
elif mode == "decode":
    print(f"v este {v}")
    decode(v, bits).tofile(output_file)

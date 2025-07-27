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

    if sys.argv[index] == "-o":
        try:
            output_file = sys.argv[index + 1]
            return index + 2
        except:
            invalid_options_message("for -o")
            exit(1)
    elif sys.argv[index] == "-l":
        try:
            bits = int(sys.argv[index + 1])
            return index + 2
        except:
            invalid_options_message("for -l")
            exit(1)
    elif sys.argv[index] == "-t":
        try:
            threads = int(sys.argv[index + 1])
            return index + 2
        except:
            invalid_options_message("for -t")
            exit(1)

    else:
        invalid_options_message(sys.argv[index])
        exit(1)

def invalid_options_message(option):
    print(f'''imgsteg: invalid option {option}\nTry \'imgsteg -h\' for more information''')

def helper():
    print('''Usage:
        encode:      imgsteg [IMAGE FILE] [SECRET FILE] [OPTIONS]
        decode:      imgsteg -d [IMAGE FILE] [OPTIONS]
    \nFlags:
        -h           This help message")
        -o string    Output file where the resulting image/message is put
        -t number    Number of threads to use for encoding/decoding
        -l number    Bits to use for hiding the message''')

def arg_parser():
    global image_file
    global data_file

    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        helper()
        exit(1)

    if len(sys.argv) < 3:
        invalid_options_message("")
        exit(1)

    if sys.argv[1] == "-d":
        image_file = sys.argv[2]
    else:
        image_file = sys.argv[1]
        data_file = sys.argv[2]

    index = 3

    while index < len(sys.argv):
        index = options(index)

def thread_encode_controller(v, s, bits, threads):
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
            t = Thread(target=thread_encoder, args=(v[image_index : image_index + (len(s) - data_index) * 8 // bits], s[data_index : len(s)], bits, thread_v[i]))
            thrs.append(t)
            t.start()
        else:
            print(f"data [{data_index}, {data_index + data_section - 1}] and image [{image_index}, {image_index + image_section - 1}]")
            t = Thread(target=thread_encoder, args=(v[image_index : image_index + image_section], s[data_index : data_index + data_section], bits, thread_v[i]))
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

def thread_encoder(v, s, bits, new_v):
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
    start_index = 8 * 8 // bits
    data_length = calculate_data_length(v[:start_index], bits)
    v = v[start_index:]

    data = []
    curr_char = 0
    bit_mask = 2 ** bits - 1
    carridge = 0

    for elem in v:
        if data_length == 0:
            break

        bit = elem & bit_mask
        curr_char = curr_char + (bit << carridge)
        carridge += bits

        if carridge >= 8:
            carridge = 0
            data.append(curr_char)
            data_length -= 1
            curr_char = 0

    return np.array(data, dtype='int')

def calculate_data_length(v, bits):
    carridge = 0
    bit_mask = 2 ** bits - 1
    bytes_vector = []
    curr_char = 0

    for elem in v:
        bit = elem & bit_mask
        curr_char = curr_char + (bit << carridge)
        carridge += bits

        if carridge >= 8:
            carridge = 0
            bytes_vector.append(curr_char)
            curr_char = 0

    return int.from_bytes(bytes(bytes_vector))

def thread_decode_controller(v, bits, threads):
    start_index = 8 * 8 // bits
    data_length = calculate_data_length(v[:start_index], bits)
    print(f"data length is {data_length}")
    v = v[start_index:]

    if data_length * 8 // bits > len(v):
        raise ValueError("The data_length extracted from the image is greater than the image size")

    thread_v = [[] for i in range(threads)]
    image_section = data_length // threads * 8 // bits
    image_index = 0
    image_size = data_length * 8 // bits

    thrs = []
    for i in range(threads):
        print(f"i este {i}")
        if image_index + 2 * image_section > image_size:
            print(f"image [{image_index}, {image_index + (image_size - image_index) - 1}]")
            t = Thread(target=thread_decoder, args=(v[image_index : image_index + (image_size - image_index)], bits, thread_v[i]))
            thrs.append(t)
            t.start()
        else:
            print(f"image [{image_index}, {image_index + image_section - 1}]")
            t = Thread(target=thread_decoder, args=(v[image_index : image_index + image_section], bits, thread_v[i]))
            thrs.append(t)
            t.start()

        image_index += image_section


    for t in thrs:
        t.join()

    data = np.array([], dtype='uint8')
    for i in range(threads):
        data = np.append(data, thread_v[i])

    return data

def thread_decoder(v, bits, data):
    curr_char = 0
    bit_mask = 2 ** bits - 1
    carridge = 0

    for elem in v:
        bit = elem & bit_mask
        curr_char = curr_char + (bit << carridge)
        carridge += bits

        if carridge >= 8:
            carridge = 0
            data.append(curr_char)
            curr_char = 0



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

    if threads == 1:
        new_v = encode(v, data, bits)
    else:
        new_v = thread_encode_controller(v, data, bits, threads)

    new_arr = new_v.reshape(arr.shape)
    new_img = Image.fromarray(new_arr)
    new_img.save(output_file)
elif mode == "decode":
    print(f"v este {v}")
    thread_decode_controller(v, bits, threads).tofile(output_file)

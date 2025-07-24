#!/bin/python3

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import random

#img = Image.open('sample.png')
#arr = np.asarray(img)
#
#print(type(arr))
#print(arr.shape)
#
#plt.imshow(arr, interpolation='nearest')
#plt.show()

#for line in arr:
#    for cell in line:
#        for elem in cell:
#            print(elem)

def encode(v, s):
    if len(s) * 8 > len(v):
        raise ValueError("Not enough bits in vector to hide message")

    new_v = []
    mask = 0b11111110
    print(list(s))
    s_list = list(s)
    total_bits = len(s) * 8
    curr_char = ord(s_list.pop(0))
    print(f"list is {s_list}, total_bits is {total_bits} and curr char is {curr_char}")

    for elem in v:
        if total_bits == 0:
            break

        elem = (elem & mask) + (curr_char & 1)
        new_v.append(elem)
        curr_char >>= 1
        total_bits -= 1

        if total_bits % 8 == 0 and total_bits != 0:
            curr_char = ord(s_list.pop(0))

    return new_v

def decode(v):
    s = []
    total_bits = len(v) - len(v) % 8
    curr_char = 0
    print(f"total_bits is {total_bits}")

    carridge = 0
    for elem in v:
        if total_bits == 0:
            break

        bit = elem & 1
        curr_char = curr_char + (bit << carridge)
        carridge += 1
        total_bits -= 1

        if carridge >= 8:
            carridge = 0
            s.append(chr(curr_char))
            curr_char = 0

    return ''.join(s)




v = [10, 11, 12, 13, 14, 15, 16, 17]
xchr = 'a'
x = ord(xchr)
mask = 0b11111110
print(f"mask: {mask} and x is {x}")

new_v = []

#encode
for num in v:
    aux = x & 1
    print(f"num was: {bin(num)}, aux is {bin(aux)}")
    num = (num & mask) + aux
    new_v.append(num)
    x = x >> 1

v = new_v
print(v)

#decode
decoded = 0
carridge = 0

for num in v:
    bit = num & 1
    decoded = decoded + (bit << carridge)
    carridge += 1

print(decoded)

v = random.sample(range(256), 256)
print(v)
new_v = encode(v, "Hello World! ce mai faci")

print(decode(new_v))

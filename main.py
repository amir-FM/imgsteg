#!/bin/python3

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import random

text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc mollis eu nisl et iaculis. Mauris tempus elit in leo mollis tincidunt. Morbi faucibus semper dui, eu rhoncus nisi vulputate non. Nunc egestas consectetur luctus. Cras cursus, velit vel tincidunt suscipit, nunc libero volutpat nisi, a finibus orci massa at sem. Cras faucibus venenatis semper. Donec luctus ipsum scelerisque leo feugiat, et mollis augue interdum. Quisque fringilla eleifend dictum. Nam pulvinar orci eros, sed imperdiet mi mollis at. Morbi felis neque, venenatis vel elit vel, blandit feugiat lectus. Quisque ultrices pharetra diam, vel sodales orci imperdiet non. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Vestibulum tincidunt lacinia tellus vel fringilla. Sed eget egestas risus. Vestibulum pharetra urna dui, et facilisis turpis tincidunt sit amet. Vestibulum rutrum eget massa ac sodales.

Maecenas sit amet velit in leo consectetur rutrum accumsan eget augue. Morbi id molestie urna, vel euismod neque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam tincidunt ipsum at facilisis facilisis. Donec mollis elementum velit, quis auctor elit pharetra vitae. Morbi nulla arcu, lobortis in vestibulum ac, volutpat sed turpis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Donec vel leo tellus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vestibulum posuere vestibulum. Curabitur ut nisi et arcu egestas dapibus. Nulla facilisi. Proin placerat turpis erat, ac dapibus nibh finibus at.

Aliquam lobortis, augue eu imperdiet maximus, sem massa tristique ligula, a suscipit nisl ligula ut turpis. Ut interdum risus vitae congue laoreet. Sed leo risus, vulputate ut arcu eu, semper pulvinar ipsum. Sed ut sapien risus. Nulla eu libero leo. Curabitur pharetra elit sit amet odio volutpat fermentum. Maecenas non mi vitae tellus egestas faucibus. In ac diam ac enim pretium gravida. In at nunc sit amet purus fringilla sollicitudin vitae tristique tellus. Pellentesque molestie turpis tortor, id congue magna gravida id. Nulla molestie pellentesque tortor, eget sodales nunc venenatis sed. Sed orci orci, ultricies et consectetur sed, sodales molestie enim. Aliquam a risus a dolor feugiat efficitur.

Etiam blandit pulvinar nunc, nec cursus nunc finibus et. Aenean posuere quis ligula nec egestas. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum est ipsum, gravida vitae tellus non, maximus egestas leo. Ut porttitor nulla orci, scelerisque porttitor libero imperdiet faucibus. Praesent efficitur metus et eros placerat ultricies. Maecenas nisi odio, malesuada a est porta, congue tincidunt augue. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Duis aliquet, mi ut faucibus imperdiet, libero lectus posuere augue, mattis fringilla risus purus id est. Morbi malesuada, odio elementum semper mattis, velit mauris malesuada sem, eu lobortis justo enim in lorem. Vivamus quam lorem, varius pellentesque euismod ac, scelerisque condimentum justo. Ut elementum euismod libero, id tempor diam viverra lacinia.

Suspendisse hendrerit purus ac consectetur euismod. Phasellus vulputate tincidunt mollis. Nunc at ipsum eget justo congue rhoncus vel et nibh. Nunc vel vulputate eros. Suspendisse sit amet fringilla mi. Pellentesque malesuada nibh arcu. Sed ultrices non turpis quis ultricies. Maecenas ligula leo, suscipit ut interdum vitae, eleifend eget dolor. Nulla id odio mollis, venenatis urna eu, rhoncus nisl. Praesent tincidunt ante eu sollicitudin porta. Integer in semper libero, in maximus ex. Duis pharetra velit sit amet velit placerat faucibus in ut nunc. Aliquam quis gravida urna, pretium sodales nibh.

Cras convallis laoreet cursus. Maecenas sit amet mollis urna, non elementum nunc. Aliquam semper magna sit amet mi aliquet, vitae viverra eros placerat. Sed blandit vehicula leo suscipit sagittis. In elementum, quam at sagittis porta, sem libero iaculis augue, ut bibendum neque lorem ac velit. Aliquam faucibus nisl nec mauris tincidunt tincidunt. Praesent placerat interdum ornare. Donec et dolor quis elit viverra auctor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec venenatis lorem eget dui condimentum accumsan. 
'''

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

    new_v = np.array([], dtype='uint8')
    mask = 0b11111110
    s_list = list(s)
    total_bits = len(s) * 8
    curr_char = ord(s_list.pop(0))
    print(f"total_bits is {total_bits} and curr char is {curr_char}")
    index = 0

    for elem in v:
        if total_bits == 0:
            break

        elem = (elem & mask) + (curr_char & 1)
        new_v = np.append(new_v, elem)
        curr_char >>= 1
        total_bits -= 1
        index += 1

        if total_bits % 8 == 0 and total_bits != 0:
            curr_char = ord(s_list.pop(0))

    print(f"index stopped at {index}")
    new_v = np.append(new_v, v[index:])
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




#v = [10, 11, 12, 13, 14, 15, 16, 17]
#xchr = 'a'
#x = ord(xchr)
#mask = 0b11111110
#print(f"mask: {mask} and x is {x}")
#
#new_v = []
#
##encode
#for num in v:
#    aux = x & 1
#    print(f"num was: {bin(num)}, aux is {bin(aux)}")
#    num = (num & mask) + aux
#    new_v.append(num)
#    x = x >> 1
#
#v = new_v
#print(v)
#
##decode
#decoded = 0
#carridge = 0
#
#for num in v:
#    bit = num & 1
#    decoded = decoded + (bit << carridge)
#    carridge += 1
#
#print(decoded)
#
#v = random.sample(range(256), 256)
#print(v)
#new_v = encode(v, "Hello World! ce mai faci")
#
#print(decode(new_v))

img = Image.open('sample.png')
arr = np.asarray(img)

print(type(arr))
print(arr.shape)

v = np.ravel(arr)
print(v.shape)

new_v = encode(v, text)
print(new_v.shape)

new_arr = new_v.reshape((1024, 1024, 4))
print(new_arr.shape)
print(arr.dtype)
print(v.dtype)
print(new_v.dtype)
print(new_arr.dtype)

plt.imshow(new_arr, interpolation='nearest')
plt.show()

print(decode(new_v))

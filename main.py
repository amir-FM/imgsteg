#!/bin/python3

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

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

v = [10, 11, 12, 13, 14, 15, 16, 17]
x = 123
mask = 0b11111110
print(f"mask: {mask} and num is {bin(x)}")

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

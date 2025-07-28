# imgsteg

Steganography software that can hide any file inside an image.

## Description

Multithreaded application based on **LSB** (Least Significant Bit) concept that
is able to hide messages with varying degrees of obfuscation. It features a
encoder as well as a decoder for easy use.

## Installation

```
git clone https://github.com/amir-FM/imgsteg [installation directory]
cd [installation directory]
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./imgsteg -h
```

## Usage examples

The examples below showcase the functionality of **imgsteg**, for furthare reading check the help menu.

### Encoding

```
imgsteg example.jpg secret.pdf -o example_out.png
```
Typical command used for a small secret file using the best encoding that marginally alters the image color bytes. For bigger secret files it is recomended to use multithreading.

### Decoding

```
imgsteg -d example_out.png -o extracted
```
*Note*: for the decoding process, from testing, the use of multithreading hidered performance slightly.

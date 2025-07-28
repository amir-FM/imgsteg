# imgsteg

Steganography software that can hide any file inside an image.

<img width="7485" height="1735" alt="collage" src="https://github.com/user-attachments/assets/0c277cfa-bed6-42dc-93fd-d5f94b378a23" />

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
<img width="565" height="91" alt="encode" src="https://github.com/user-attachments/assets/0d7451d7-c933-459d-80dd-92b5a625327f" />

Typical command used for a small secret file using the best encoding that marginally alters the image color bytes. For bigger secret files it is recomended to use multithreading.

### Decoding

```
imgsteg -d example_out.png -o extracted
```
<img width="478" height="71" alt="decode" src="https://github.com/user-attachments/assets/74120eff-f9c6-41f2-9d9a-ab4332204a5c" />

*Note*: for the decoding process, from testing, the use of multithreading hidered performance slightly.

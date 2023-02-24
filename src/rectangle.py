# importing image object from PIL
import math
from PIL import Image, ImageDraw
from pathlib import Path
import numpy as np
from src.qr import print_qr, write_qr

from PIL import Image, ImageFont, ImageDraw, ImageOps
import os 
import cv2
font_path = os.path.join(cv2.__path__[0],'qt','fonts','DejaVuSans.ttf')


def cm_to_pixels(cm: float) -> int:
    return int(cm * 37.79527559055118)


# get index of all the spaces
def split_long_string(string, max_len_per_row=25):
    """Max len per row is 25 characters"""
    if len(string) > max_len_per_row*2:
        raise ValueError("String too long")
    idx_spaces = [i for i, x in enumerate(string) if x == ' ' and i < max_len_per_row]
    last_idx_before_split = idx_spaces[-1]
    first_part = string[:last_idx_before_split]
    second_part = string[last_idx_before_split+1:] # +1 to remove the space
    print(f'first_part: "{first_part}" second_part: "{second_part}"')
    return first_part, second_part



cm_w = 2.9
cm_h = 5 # this is the length of the lable

w, h = cm_to_pixels(cm=cm_w), cm_to_pixels(cm=cm_h)
shape = [(40, 40), (w - 10, h - 10)]
  
# creating new Image object
img = Image.new("RGB", (w, h), color='white')


out_fp = f'temp_/QR_11_print.png'
Path(out_fp).unlink(missing_ok=True)
img.save(out_fp)

qr_out = write_qr(mac='test', box_size=2.5)
qr_img = Image.open(qr_out)



img.paste(qr_img, (40, 0), qr_img.convert('RGBA'))

# text
# on top of the QR code
mac = 'B8D61A188B2C'
font = ImageFont.truetype(font_path, size=15)


img = img.rotate(angle=90, expand=True)
d = ImageDraw.Draw(img)

# Get width and height of text
w, h = d.textsize(mac, font=font)

#  add MAC address
width_and_height = (60, 8)
print(width_and_height)
d.text(width_and_height, 
       mac, 
       font=font, fill='black')

## add address and city
address = "this could be a long address like very long"
width_and_height = (8, 60)

second_part = None
if len(address) > 25:
    first_part, second_part = split_long_string(address)
else:
    # address is short
    first_part = address
    
d.text(width_and_height, 
       first_part, 
       font=font, fill='black')

if second_part:
    width_and_height = (8, 75)
    d.text(width_and_height, 
        second_part, 
        font=font, fill='black')

# add last part of address, the city
width_and_height = (8, 90)

d.text(width_and_height,
       "Rotterdam", 
       font=font, fill='black')

# img.show()

out_print = f'temp_/QR_11_print.png'
img = img.rotate(angle=-90, expand=True)

img.show()
img.save(out_print)
print_qr(img_fp=out_print)
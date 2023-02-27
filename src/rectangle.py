# importing image object from PIL
import math
from PIL import Image, ImageDraw
from pathlib import Path
import numpy as np
from src.qr import print_qr, write_qr, make_qr_img

from PIL import Image, ImageFont, ImageDraw, ImageOps
import os


def cm_to_pixels(cm: float) -> int:
    return int(cm * 37.79527559055118)


def create_background_image(cm_width: float,
                            cm_height: float,
) -> Image.Image:
    w, h = cm_to_pixels(cm=cm_w), cm_to_pixels(cm=cm_h)
    # creating new Image object
    img = Image.new("RGB", (w, h), color='white')
    return img


# get index of all the spaces
def split_long_string(string, max_len_per_row=25):
    """Max len per row is 25 characters"""
    if len(string) > max_len_per_row*2:
        raise ValueError("String too long")
    idx_spaces = [i for i, x in enumerate(string) 
                  if x == ' ' and i < max_len_per_row]
    last_idx_before_split = idx_spaces[-1]
    first_part = string[:last_idx_before_split]
    second_part = string[last_idx_before_split+1:] # +1 to remove the space
    print(f'first_part: "{first_part}" second_part: "{second_part}"')
    return first_part, second_part


def get_default_text_kwargs()-> dict:
    """Gets font and color for the text"""
    font_path = 'assets/LucidaSansRegular.ttf'
    font = ImageFont.truetype(font_path, size=15)
    text_kwargs = dict(font=font, fill='black')
    return text_kwargs


cm_w = 2.9
cm_h = 5 # this is the length of the lable
mac = 'B8D61A188B2C'
## add address and city
address = "this could be a long address like very long"

city = 'Rotterdam' # add check max 25 chars



qr_img = make_qr_img(mac=mac)
img = create_background_image(cm_width=cm_w, cm_height=cm_h)
img.paste(qr_img, (40, 0), qr_img.convert('RGBA'))



""" rotate as the original img is vertical
    TODO probably you can do this in a better way, by creating
    an horizontal image from the beginning
"""
img.show(title = 'before rotation')
img = img.rotate(angle=90, expand=True)
d = ImageDraw.Draw(img)

#  add MAC address (width, height in pixels)
width_and_height = (68, 2)

print(width_and_height)
text_kwargs = get_default_text_kwargs()
d.text(width_and_height,
       mac,
       **text_kwargs)


second_part = None
if len(address) > 25:
    first_part, second_part = split_long_string(address)
else:
    # address is short
    first_part = address

width_and_height = (8, 60)
d.text(width_and_height, 
       first_part, 
       **text_kwargs)

if second_part:
    width_and_height = (8, 75)
    d.text(width_and_height, 
           second_part, 
           **text_kwargs)

# add last part of address, the city
width_and_height = (8, 90)

d.text(width_and_height,
       city, 
       **text_kwargs)

out_print = f'temp_/QR_11_print.png'
img = img.rotate(angle=-90, expand=True)

# img.show()
img.save(out_print)
print_qr(img_fp=out_print)
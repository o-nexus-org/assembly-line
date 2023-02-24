""" 
requirements.txt

qrcode==7.4.2
Pillow==8.1.0
opencv-python==4.7.0.68
wand=0.6.11
"""
import os
from pathlib import Path

import cv2
import qrcode
from PIL import Image, ImageFont, ImageDraw, ImageOps


def create_qr_img(box_size: int) -> str:
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
    )
    url = 'google.com'
    QRcode.add_data(url)
    QRcode.make()
    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color='Black', back_color="white").convert('RGB')
    # save the QR code generated
    out_fp = f'temp_/QR.png'
    QRimg.save(out_fp)
    return out_fp

def add_str_to_img(img_path: str, 
                               str1: str,
                               str2: str,
                               show:bool=False) -> str:

    black_color_rgb = (0,0,0)
    white_color_rgb = (255,255,255)
    img = Image.open(img_path)
    
    #failed attempt 1)
    # expanding the border works only for writing on top or under the QR code
    # but if the string is too long, it gets cut off
    img = ImageOps.expand(img, border=30, fill=white_color_rgb)

    
    # failed attempt 2)
    # add empty space to the left of the QR code
    # exp_cm = 3
    # exp_px = int(exp_cm * 37.79527559055118)
    # new_shape_pixels = (img.width+exp_px, img.height)
    # img = ImageOps.fit(img, new_shape_pixels, method=Image.ANTIALIAS,
    #              #bleed=0.0, centering=(0.5, 0.5)
    # )
    # end failed attempt 2)
    draw = ImageDraw.Draw(img)
    font_path = os.path.join(cv2.__path__[0],'qt','fonts','DejaVuSans.ttf')
    font = ImageFont.truetype(font_path, size=52)
    # on top of the QR code
    draw.text((62,0),str1,(0,0,0),font=font,
              align='center'
            )
    # bottom
    draw.text((0,470),str2,black_color_rgb,font=font,
              align='center',
              )
    print('QR code TO BE generated!')
    out_fp = f'temp_/QR_print.png'
    Path(out_fp).unlink(missing_ok=True)
    img.save(out_fp)
    if show:
        img.show()
    print('QR code generated!')
    return out_fp

def break_fix(text, width, font, draw):
    if not text:
        return
    lo = 0
    hi = len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = text[:mid]
        w, h = draw.textsize(t, font=font)
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = text[:lo]
    w, h = draw.textsize(t, font=font)
    yield t, w, h
    yield from break_fix(text[lo:], width, font, draw)

def fit_text(img, text, color, font):
    width = img.size[0] - 2
    draw = ImageDraw.Draw(img)
    pieces = list(break_fix(text, width, font, draw))
    height = sum(p[2] for p in pieces)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")
    y = (img.size[1] - height) // 2
    for t, w, h in pieces:
        x = (img.size[0] - w) // 2
        draw.text((x, y), t, font=font, fill=color)
        y += h


if __name__ == '__main__':
    img_path = create_qr_img()
    # add_str_to_img(img_path, 
    #                'ExampleAboveQr', 
    #                'This is some long string. It could be multi-line. 22222222', 
    #                show=True)
    img = Image.open(img_path)
    img = Image.new('RGB', (128, 48), color='black')
    font_path = os.path.join(cv2.__path__[0],'qt','fonts','DejaVuSans.ttf')
    font = ImageFont.truetype(font_path, size=52)
    img_fit = fit_text(img, 'LongerTextGoesHere', (255,255,0), font)
    img_fit.show()
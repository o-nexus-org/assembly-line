""" 
Code to generate PR code.
"""
from pathlib import Path
import cv2
import os
import subprocess
import qrcode
from PIL import Image, ImageFont, ImageDraw, ImageOps
from src.utils import run_bash 



def write_qr(mac) -> str:
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    url = f'https://afmelden.o-nexus.com/?mac={mac}'
    QRcode.add_data(url)
    QRcode.make()
    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color='Black', back_color="white").convert('RGB')
    # save the QR code generated
    out_fp = f'temp_/QR_{mac}.png'
    QRimg.save(out_fp)
    return out_fp


def add_mac_and_address_to_img(img_path: str, 
                               mac: str,
                               address: str,
                               show:bool=False) -> str:
    if len(address) > 20:
        raise RuntimeError("Address too long, NOT SUPPORTED")

    black_color_rgb = (0,0,0)
    white_color_rgb = (255,255,255)
    img = Image.open(img_path)
    img = ImageOps.expand(img, border=19, fill=white_color_rgb)
    draw = ImageDraw.Draw(img)
    font_path = os.path.join(cv2.__path__[0],'qt','fonts','DejaVuSans.ttf')
    font = ImageFont.truetype(font_path, size=52)
    # on top of the QR code
    draw.text((62,0),mac,(0,0,0),font=font,
              align='center'
            )
    # bottom
    draw.text((0,470),address,black_color_rgb,font=font,
              align='center',
              )
    out_fp = f'temp_/QR_{mac}_print.png'
    Path(out_fp).unlink(missing_ok=True)
    img.save(out_fp)
    if show:
        img.show() 
    print('QR code generated!')
    return out_fp


def create_qr(mac: str, 
              address: str,
              show: bool=False) -> str:
    out_fp = write_qr(mac=mac)
    out_fp = add_mac_and_address_to_img(img_path=out_fp, 
                                        mac=mac,
                                        address=address,
                                        show=show)
    return out_fp


def print_qr(img_fp: str, n_copy: int = 1):
    first_part_usb_cmd = "lsusb | grep Brother | cut -d ' ' -f6 | cut -d ':' -f1 "
    first_part_usb = run_bash(first_part_usb_cmd)
    sec_part_usb_cmd = "lsusb | grep Brother | cut -d ' ' -f6 | cut -d ':' -f2 "
    sec_part_usb = run_bash(sec_part_usb_cmd)
    print(f"{first_part_usb} {sec_part_usb}")
    cmd = f"brother_ql -p 'usb://0x{first_part_usb}:0x{sec_part_usb}' -b pyusb --model QL-700 print --label 29 {img_fp}"
    while n_copy > 0:
        out =  run_bash(cmd)
        n_copy -= 1
        print(out)
    

def create_and_print_qr(mac: str, 
                        address: str,
                        n_copy: int = 1) -> str:
    out_fp = create_qr(mac=mac, address=address, show=False)
    print_qr(img_fp=out_fp, n_copy=n_copy)
    return out_fp


if __name__ == "__main__":

    mac = "B8D61A188B2C"
    address = "Govert Flinkstraat 7"
    out_fp = create_qr(mac=mac, address=address, show=True)
    print_qr(img_fp=out_fp)



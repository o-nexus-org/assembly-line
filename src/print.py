

from typing import Optional
from Pil import Image
from src.utils import run_bash, get_random_string


def print_img(img_fp: Optional[str],
              img: Optional[Image.Image],
              n_copy: int = 1):
    first_part_usb_cmd = "lsusb | grep Brother | cut -d ' ' -f6 | cut -d ':' -f1 "
    first_part_usb = run_bash(first_part_usb_cmd)
    sec_part_usb_cmd = "lsusb | grep Brother | cut -d ' ' -f6 | cut -d ':' -f2 "
    sec_part_usb = run_bash(sec_part_usb_cmd)
    if first_part_usb == '' or sec_part_usb == '':
        raise RuntimeError("No Brother printer found!")
    if img_fp:
        pass
    elif img is not None:
        random_str = get_random_string(5)
        out_print = f'temp_/QR_{random_str}_print.png'
        img.save(out_print)
        img_fp = out_print
    cmd = f"brother_ql -p 'usb://0x{first_part_usb}:0x{sec_part_usb}' -b pyusb --model QL-700 print --label 29 {img_fp}"
    while n_copy > 0:
        out = run_bash(cmd)
        n_copy -= 1
        print(out)

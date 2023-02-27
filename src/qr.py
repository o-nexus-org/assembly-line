"""
Code to generate PR code.
"""
import qrcode
from PIL import Image


def write_qr(mac, box_size: int) -> str:
    """
    https://pypi.org/project/qrcode/
    box_size means how many pixels each box of the QR code will be
    """
    QRcode = qrcode.QRCode(
        # ref https://www.qrcode.com/en/about/error_correction.html
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
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


def make_qr_img(mac: str, box_size: int = 3) -> Image.Image:
    qr_out = write_qr(mac=mac, box_size=box_size)
    qr_img = Image.open(qr_out)
    qr_img = qr_img.resize((70, 70))
    return qr_img

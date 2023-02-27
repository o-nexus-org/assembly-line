from src.qr import make_qr_img


def test_qr_code_has_constant_size():
    """This ensures a constant size of the QR code, regardless of the content"""
    img1 = make_qr_img("a very long mac address", box_size=3)
    img2 = make_qr_img("test", box_size=3)
    assert img1.size == img2.size


from PIL import Image, ImageFont, ImageDraw
from src.qr import make_qr_img


def cm_to_pixels(cm: float) -> int:
    return int(cm * 37.79527559055118)


def create_background_image(cm_width: float,
                            cm_height: float,
    ) -> Image.Image:
    w, h = cm_to_pixels(cm=cm_width), cm_to_pixels(cm=cm_height)
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
    second_part = string[last_idx_before_split+1:]  # +1 to remove the space
    print(f'first_part: "{first_part}" second_part: "{second_part}"')
    return first_part, second_part


def get_default_text_kwargs() -> dict:
    """Gets font and color for the text"""
    font_path = 'assets/LucidaSansRegular.ttf'
    font = ImageFont.truetype(font_path, size=15)
    text_kwargs = dict(font=font, fill='black')
    return text_kwargs


def add_text_img(image_draw: ImageDraw.ImageDraw,
                 widht_and_height_pixels: tuple,
                 text: str,
                 text_kwargs: dict = get_default_text_kwargs()
                 ) -> None:
    image_draw.text(widht_and_height_pixels,
                    text,
                    **text_kwargs)


def add_text_address_img(image_draw: ImageDraw.ImageDraw,
                         address: str,
                         text_kwargs: dict = get_default_text_kwargs()
                         ) -> None:
    """Adds the address to the image"""
    second_part = None
    if len(address) > 25:
        first_part, second_part = split_long_string(address)
    else:
        # address is short
        first_part = address

    add_text_img(image_draw=image_draw,
                 widht_and_height_pixels=(8, 60),
                 text=first_part)
    if second_part:
        add_text_img(image_draw=image_draw,
                     widht_and_height_pixels=(8, 75),
                     text=second_part)


def create_label_png(mac: str, address: str, city: str,
                     cm_width: float = 5,
                     cm_height: float = 2.9) -> Image.Image:

    if len(mac) > 12:
        raise ValueError("MAC address too long")
    if len(city) > 25:
        raise NotImplementedError("City name too long, needs implementation")
    if len(address) > 45:
        raise NotImplementedError("Address too long, needs implementation")

    qr_img = make_qr_img(mac=mac)
    img = create_background_image(cm_width=cm_width, cm_height=cm_height)
    img.paste(qr_img, (2, 0), qr_img.convert('RGBA'))
    d = ImageDraw.Draw(img)
    add_text_img(image_draw=d,
                 widht_and_height_pixels=(68, 2),
                 text=mac)
    add_text_address_img(image_draw=d, address=address)
    add_text_img(image_draw=d,
                 widht_and_height_pixels=(8, 90),
                 text=city)
    # necessary for printing
    img = img.rotate(angle=-90, expand=True)
    return img


if __name__ == '__main__':
    # params
    mac = 'B8D61A188B2C'
    address = "this could be a long address like very long"""
    city = 'Rotterdam'
    label_img = create_label_png(mac=mac, address=address, city=city)

    from src.print import print_img
    print_img(img_fp=None, img=label_img, n_copy=1)

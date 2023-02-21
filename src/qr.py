import pyqrcode
from PIL import Image

url = pyqrcode.QRCode('https://afmelden.o-nexus.com/?gw=B8D61A188B2C',error = 'H')
img_path = 'logo.png'
url.png('test.png',scale=10)
im = Image.open('test.png')
im = im.convert("RGBA")
logo = Image.open('logo.png')
box = (135,135,235,235)
im.crop(box)
region = logo
region = region.resize((box[2] - box[0], box[3] - box[1]))
im.paste(region,box)
im.show()
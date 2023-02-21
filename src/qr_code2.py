""" 
You may want to delete this file!

"""
# import modules
# https://www.geeksforgeeks.org/how-to-generate-qr-codes-with-a-custom-logo-using-python/
import qrcode
from PIL import Image
 
 
def make_background_white(image: Image) -> Image:
    new_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
    new_image.paste(image, (0, 0), image)              # Paste the image on the background. Go to the links given below for details.
    new_image = new_image.convert('RGB')
    return new_image


# taking image which user wants
# in the QR code center
Logo_link = 'logo.png'
 
logo = Image.open(Logo_link)
 
# taking base width
basewidth = 100
 
# adjust image size
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
logo = make_background_white(logo)
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
 
# taking url or text
url = 'https://afmelden.o-nexus.com/?gw=B8D61A188B2C'
 
# adding URL or text to QRcode
QRcode.add_data(url)
 
# generating QR code
QRcode.make()
 
# taking color name from user
QRcolor = 'Black'
 
# adding color to QR code
QRimg = QRcode.make_image(
    fill_color=QRcolor, back_color="white").convert('RGB')
 
# set size of QR code
# pos = ((QRimg.size[0] - logo.size[0]) // 2,
#        (QRimg.size[1] - logo.size[1]) // 2)
# QRimg.paste(logo, pos)
 
# save the QR code generated
QRimg.save('test_QR.pdf')
 
print('QR code generated!')
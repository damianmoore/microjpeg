import struct
import StringIO

from PIL import Image


def generate_microjpeg(width=48, height=48, quality=10):

    header = open('headers/header.bin', 'rb').read()

    img_file = StringIO.StringIO()
    im = Image.open('samples/flowers_square.jpg')
    im.thumbnail((width, height), Image.ANTIALIAS)
    im.save(img_file, 'JPEG', quality=10)

    img_file.seek(0)
    img_data = img_file.read()

    header_offset = len(header) + 4  # 4 bytes for width and height

    with open('microjpegs/body.bin', 'wb') as output:
        # microjpeg header
        output.write(struct.pack('>H', 0)[1])       # version number (byte 0)
        output.write(struct.pack('>H', quality)[1]) # quality (byte 1)
        output.write(struct.pack('>H', width)[1])   # width (byte 2)
        output.write(struct.pack('>H', height)[1])  # height (byte 3)
        # microjpeg body
        output.write(img_data[header_offset:])

    bytes_out = len(open('microjpegs/body.bin').read())
    print('Wrote microjpeg (microjpegs/body.bin {} bytes)'.format(bytes_out))


if __name__ == '__main__':
    generate_microjpeg()

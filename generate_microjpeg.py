import struct
import StringIO

from PIL import Image


def generate_microjpeg(width=48, height=48, quality=10):
    # Get JPEG header and our own headers within it
    header = open('headers/header.bin', 'rb').read()
    header = header[17:]
    header_quality = struct.unpack('>H', '\x00' + header[1])[0]
    header = header[3:]

    # Read the full-size image and make a small JPEG of in memory
    img_file = StringIO.StringIO()
    im = Image.open('samples/flowers_square.jpg')
    im.thumbnail((width, height), Image.ANTIALIAS)
    assert(header_quality == quality)
    im.save(img_file, 'JPEG', quality=quality)

    img_file.seek(0)
    img_data = img_file.read()

    # Based on the existing JPEG header file, work out where the unique part of
    # our new in-memory thumbnail starts
    header_offset = len(header) + 4  # 4 bytes for width and height

    # Write out the unique part with out own 4 byte header
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

import argparse
import os
import struct
import StringIO

from PIL import Image


def generate_microjpeg(path, version=0, size=48, quality=10):
    width = height = size

    # Get JPEG header and our own headers within it
    fn = 'headers/header_v0_q{}.bin'.format(quality)
    try:
        header = open(fn, 'rb').read()
    except IOError:
        raise IOError('No header file found for quality {}. You need to generate one first with generate_header.py'.format(quality))
    header = header[17:]
    header_quality = struct.unpack('>H', '\x00' + header[1])[0]
    header = header[3:]

    # Read the full-size image and make a small JPEG of in memory
    img_file = StringIO.StringIO()
    im = Image.open(path)
    im.thumbnail((width, height), Image.ANTIALIAS)
    assert(header_quality == quality)
    im.save(img_file, 'JPEG', quality=quality)

    img_file.seek(0)
    img_data = img_file.read()

    # Based on the existing JPEG header file, work out where the unique part of
    # our new in-memory thumbnail starts
    header_offset = len(header) + 4  # 4 bytes for width and height

    # Write out the unique part with out own 4 byte header
    fn = os.path.join('microjpegs', os.path.splitext(os.path.split(path)[-1])[0] + '.microjpeg')
    with open(fn, 'wb') as output:
        # microjpeg header
        output.write(struct.pack('>H', 0)[1])       # version number (byte 0)
        output.write(struct.pack('>H', quality)[1]) # quality (byte 1)
        output.write(struct.pack('>H', width)[1])   # width (byte 2)
        output.write(struct.pack('>H', height)[1])  # height (byte 3)
        # microjpeg body
        output.write(img_data[header_offset:])

    bytes_out = len(open(fn).read())
    print('Wrote microjpeg ({} {} bytes)'.format(fn, bytes_out))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a microjpeg based on a pre-generated, re-usable header.')
    parser.add_argument('path', help='The path of the image to read and make into a microjpeg thumbnail.')
    parser.add_argument('-s', '--size', type=int, help='Maximum width/height to use for the thumbnail size. A multiple of 8 is most efficient.')
    parser.add_argument('-q', '--quality', type=int, help='Quality value to use for the JPEG compression. All images must have the save quality value to use the same header.')
    args = parser.parse_args()

    size = getattr(args, 'size') or 48
    quality = getattr(args, 'quality') or 10
    generate_microjpeg(args.path, size=size, quality=quality)

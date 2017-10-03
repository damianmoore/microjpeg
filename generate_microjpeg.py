import argparse
import os
import struct
import StringIO

from utils.qtables import load_qtable
from utils.resize import pil_resize, pil_gamma_resize, pil_profiled_resize, imagemagick_resize


IMAGE_PROCESSOR = 'pil'
# IMAGE_PROCESSOR = 'pil_gamma'
# IMAGE_PROCESSOR = 'pil_profiled'
# IMAGE_PROCESSOR = 'imagemagick'


def get_jpeg_data(path, qtable, size):
    # Read the full-size image and make a small JPEG of it in memory
    if qtable not in ['keep', 'web_low', 'web_high']:
        qtable = load_qtable(qtable)

    img_file = StringIO.StringIO()
    if IMAGE_PROCESSOR == 'pil':
        im = pil_resize(path, size)
    elif IMAGE_PROCESSOR == 'pil_gamma':
        im = pil_gamma_resize(path, size)
    elif IMAGE_PROCESSOR == 'pil_profiled':
        im = pil_profiled_resize(path, size)
    elif IMAGE_PROCESSOR == 'imagemagick':
        im = imagemagick_resize(path, size)
    height, width = im.size
    im.save(img_file, 'JPEG', qtables=qtable)

    img_file.seek(0)
    img_data = img_file.read()

    return img_data, width, height


def generate_microjpeg(path, qtable, size=48):
    # Get JPEG header and our own headers within it
    fn = 'headers/header_{}.bin'.format(qtable)
    try:
        header = open(fn, 'rb').read()
    except IOError:
        raise IOError('No header file found for qtable {}. You need to generate one first with generate_header.py'.format(qtable))
    header = header[1:]

    img_data, width, height = get_jpeg_data(path, qtable, size)

    # Based on the existing JPEG header file, work out where the unique part of
    # our new in-memory thumbnail starts
    header_offset = len(header) + 4  # 4 bytes for width and height

    with open('/tmp/test.jpg', 'wb') as output:
        output.write(img_data)

    # Write out the unique part with our own header
    fn = os.path.join('microjpegs', '{}_{}.microjpeg'.format(os.path.splitext(os.path.split(path)[-1])[0], qtable))
    with open(fn, 'wb') as output:
        # microjpeg header
        output.write(struct.pack('>H', width)[1])   # width (byte 2)
        output.write(struct.pack('>H', height)[1])  # height (byte 3)
        # microjpeg body
        output.write(img_data[header_offset:])

    bytes_out = len(open(fn).read())
    print('Wrote microjpeg ({} {} bytes)'.format(fn, bytes_out))
    return fn, bytes_out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a microjpeg based on a pre-generated, re-usable header.')
    parser.add_argument('path', help='The path of the image to read and make into a microjpeg thumbnail.')
    parser.add_argument('-s', '--size', type=int, help='Maximum width/height to use for the thumbnail size. A multiple of 8 is most efficient.')
    parser.add_argument('-q', '--qtable', type=int, help='Quantization table to use for the JPEG compression.')
    args = parser.parse_args()

    size = getattr(args, 'size') or 48
    qtable = getattr(args, 'qtable') or None
    generate_microjpeg(args.path, qtable=qtable, size=size)

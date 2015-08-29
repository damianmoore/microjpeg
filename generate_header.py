import argparse
import struct
import StringIO

from PIL import Image


def generate_header(version=0, quality=10):
    # Create two in-memory JPEGs that vary in dimensions and pixel colours but
    # have identical headers/DCT as they use the same quality parameter
    sample0 = StringIO.StringIO()
    im = Image.new('RGB', (1, 1), 'white')
    im.save(sample0, 'JPEG', quality=quality)
    sample0.seek(0)
    data0 = sample0.read()

    sample1 = StringIO.StringIO()
    im = Image.new('RGB', (2, 2), 'black')
    im.save(sample1, 'JPEG', quality=quality)
    sample1.seek(0)
    data1 = sample1.read()

    # Walk through both files simultaneously. The byte before where we hit the
    # first difference will be where the width and height values get set. When
    # we hit the next difference we will have got to the end of the EXIF and
    # DCT headers where the actual blocks start.
    header_bytes = StringIO.StringIO()
    dimension_loc = 0

    for i, byte in enumerate(data0):
        if dimension_loc and i < dimension_loc + 4:
            continue

        if byte != data1[i]:
            if not dimension_loc:
                dimension_loc = i - 1
                header_bytes.seek(i - 1)
                continue
            else:
                break
        else:
            header_bytes.write(byte)

    # We add our own header to the JPEG header which contains version number,
    # quality used, and the byte number position where width and height need to
    # be inserted.
    microjpeg_header = b'microjpeg header ' + struct.pack('>H', 0)[1] + struct.pack('>H', quality)[1] + struct.pack('>H', dimension_loc)[1]

    header_bytes.seek(0)
    fn = 'headers/header_v0_q{}.bin'.format(quality)
    with open(fn, 'wb') as header:
        header.write(microjpeg_header)
        header.write(header_bytes.read())

    bytes_out = len(open(fn).read())
    print('Wrote header file ({} {} bytes)'.format(fn, bytes_out))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate re-usable JPEG header.')
    parser.add_argument('-q', '--quality', type=int, help='Quality value to use for the JPEG compression. All images must have the save quality value to use the same header.')
    args = parser.parse_args()

    quality = getattr(args, 'quality') or 10
    generate_header(quality=quality)

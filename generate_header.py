import struct
import StringIO

from PIL import Image


def generate_header(version=0, quality=10):

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

    header_bytes.seek(0)
    with open('headers/header.bin', 'wb') as header:
        header.write(header_bytes.read())

    with open('headers/header.txt', 'w') as header:
        header.write('{}'.format(dimension_loc))

    bytes_out = len(open('headers/header.bin').read())
    print('Wrote header file (headers/header.bin {} bytes)'.format(bytes_out))


if __name__ == '__main__':
    generate_header()

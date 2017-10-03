import os
import argparse
import struct


def generate_jpeg(path, qtable, size):
    # Get JPEG body and our own headers within it
    body = open(path, 'rb').read()
    width = height = size

    # Get JPEG header and our own headers within it
    header_fn = 'headers/header_{}.bin'.format(qtable)
    try:
        header = open(header_fn, 'rb').read()
    except IOError:
        raise IOError('No header file found for qtable {}. It should be located at: {}'.format(qtable, header_fn))
    dimension_loc = struct.unpack('>H', '\x00' + header[0])[0]
    header = header[1:]

    # Write preview JPEG using the pre-stored header with our width/height
    # values inserted in the right place, then the unique image body
    fn = os.path.join('jpegs', '{}_s{}.jpg'.format(os.path.splitext(os.path.split(path)[-1])[0], max([width, height])))
    with open(fn, 'wb') as output:
        output.write(header[:dimension_loc])
        output.write(struct.pack('>H', width))
        output.write(struct.pack('>H', height))
        output.write(header[dimension_loc:])
        output.write(body[2:])

    bytes_out = len(open(fn).read())
    print('Wrote full jpeg from header and microjpeg ({} {} bytes)'.format(fn, bytes_out))
    return fn, bytes_out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates full JPEG from a microjpeg.')
    parser.add_argument('path', help='The path of the microjpeg to read and expand into a full JPEG.')
    args = parser.parse_args()

    generate_jpeg(args.path)

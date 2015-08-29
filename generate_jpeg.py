import os
import argparse
import struct


def generate_jpeg(path):
    # Get JPEG body and our own headers within it
    body = open(path, 'rb').read()
    body_version = struct.unpack('>H', '\x00' + body[0])[0]
    body_quality = struct.unpack('>H', '\x00' + body[1])[0]
    width = struct.unpack('>H', '\x00' + body[2])[0]
    height = struct.unpack('>H', '\x00' + body[3])[0]

    # Get JPEG header and our own headers within it
    header_fn = 'headers/header_v0_q{}.bin'.format(body_quality)
    try:
        header = open(header_fn, 'rb').read()
    except IOError:
        raise IOError('No header file found for quality {}. It should be located at: {}'.format(body_quality, header_fn))
    header = header[17:]
    header_version = struct.unpack('>H', '\x00' + header[0])[0]
    header_quality = struct.unpack('>H', '\x00' + header[1])[0]
    dimension_loc = struct.unpack('>H', '\x00' + header[2])[0]
    header = header[3:]

    assert(header_version == body_version)
    assert(header_quality == body_quality)

    # Write preview JPEG using the pre-stored header with our width/height
    # values inserted in the right place, then the unique image body
    fn = os.path.join('jpegs', os.path.splitext(os.path.split(path)[-1])[0] + '.jpg')
    with open(fn, 'wb') as output:
        output.write(header[:dimension_loc])
        output.write(struct.pack('>H', width))
        output.write(struct.pack('>H', height))
        output.write(header[dimension_loc:])
        output.write(body[4:])

    bytes_out = len(open(fn).read())
    print('Wrote full jpeg from header and microjpeg ({} {} bytes)'.format(fn, bytes_out))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates full JPEG from a microjpeg.')
    parser.add_argument('path', help='The path of the microjpeg to read and expand into a full JPEG.')
    args = parser.parse_args()

    generate_jpeg(args.path)

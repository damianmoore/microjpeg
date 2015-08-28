import struct


def generate_jpeg():
    # Get JPEG header and our own headers within it
    header = open('headers/header.bin', 'rb').read()
    header = header[17:]
    header_version = struct.unpack('>H', '\x00' + header[0])[0]
    header_quality = struct.unpack('>H', '\x00' + header[1])[0]
    dimension_loc = struct.unpack('>H', '\x00' + header[2])[0]
    header = header[3:]

    # Get JPEG body and our own headers within it
    body = open('microjpegs/body.bin', 'rb').read()
    body_version = struct.unpack('>H', '\x00' + body[0])[0]
    body_quality = struct.unpack('>H', '\x00' + body[1])[0]
    width = struct.unpack('>H', '\x00' + body[2])[0]
    height = struct.unpack('>H', '\x00' + body[3])[0]

    assert(header_version == body_version)
    assert(header_quality == body_quality)

    # Write preview JPEG using the pre-stored header with our width/height
    # values inserted in the right place, then the unique image body
    with open('jpegs/output.jpg', 'wb') as output:
        output.write(header[:dimension_loc])
        output.write(struct.pack('>H', width))
        output.write(struct.pack('>H', height))
        output.write(header[dimension_loc:])
        output.write(body[4:])

    bytes_out = len(open('jpegs/output.jpg').read())
    print('Wrote full jpeg from header and microjpeg (jpegs/output.jpg {} bytes)'.format(bytes_out))


if __name__ == '__main__':
    generate_jpeg()

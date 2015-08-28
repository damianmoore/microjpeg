import struct


def generate_jpeg():
    header = open('headers/header.bin', 'rb').read()
    body = open('microjpegs/body.bin', 'rb').read()

    width = struct.unpack('>H', '\x00' + body[2])[0]
    height = struct.unpack('>H', '\x00' + body[3])[0]

    dimension_loc = int(open('headers/header.txt', 'rb').read())

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

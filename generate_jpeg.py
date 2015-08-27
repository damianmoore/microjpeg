import StringIO

from PIL import Image


def generate_jpeg():

    header = open('headers/header.bin', 'rb').read()
    body = open('microjpegs/body.bin', 'rb').read()

    with open('jpegs/output.jpg', 'wb') as output:
        output.write(header)
        output.write(body)

    print('Wrote full jpeg from header and microjpeg (jpegs/output.jpg {} bytes)'.format(len(header) + len(body)))


if __name__ == '__main__':
    generate_jpeg()

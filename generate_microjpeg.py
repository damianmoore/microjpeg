import StringIO

from PIL import Image


def generate_microjpeg(width=40, height=40):

    header = open('headers/header.bin', 'rb').read()

    img_file = StringIO.StringIO()
    im = Image.open('samples/40x40_flowers.jpg')
    im.thumbnail((width, height), Image.ANTIALIAS)
    im.save(img_file, 'JPEG', quality=10)

    img_file.seek(0)
    img_data = img_file.read()

    # if img_data[:len(header)] != header:
    #     raise AssertionError('Generated thumbnail header does not match the pre-generated header.bin')

    header_offset = len(header) + 4  # 4 bytes for width and height

    with open('microjpegs/body.bin', 'wb') as output:
        output.write(img_data[header_offset:])

    bytes_out = len(open('microjpegs/body.bin').read())
    print('Wrote microjpeg (microjpegs/body.bin {} bytes)'.format(bytes_out))


if __name__ == '__main__':
    generate_microjpeg()

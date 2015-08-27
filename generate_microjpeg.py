import StringIO

from PIL import Image


def generate_microjpeg():

    header = open('headers/header.bin', 'rb').read()

    img_file = StringIO.StringIO()
    im = Image.open('samples/40x40_flowers.jpg')
    im.thumbnail((40, 40), Image.ANTIALIAS)
    im.save(img_file, 'JPEG', quality=10)

    img_file.seek(0)
    img_data = img_file.read()

    if img_data[:len(header)] != header:
        raise AssertionError('Generated thumbnail header does not match the pre-generated header.bin')

    with open('microjpegs/body.bin', 'wb') as output:
        output.write(img_data[len(header):])

    print('Wrote microjpeg (microjpegs/body.bin {} bytes)'.format(len(img_data) - len(header)))


if __name__ == '__main__':
    generate_microjpeg()

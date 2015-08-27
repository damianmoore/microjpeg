import StringIO

from PIL import Image


def generate_header():

    sample0 = StringIO.StringIO()
    im = Image.new('RGB', (40, 40), 'white')
    im.save(sample0, 'JPEG', quality=10)

    sample1 = StringIO.StringIO()
    im = Image.new('RGB', (40, 40), 'black')
    im.save(sample1, 'JPEG', quality=10)


    sample0.seek(0)
    data0 = sample0.read()

    sample1.seek(0)
    data1 = sample1.read()

    cutt_off = 0

    for i, byte in enumerate(data0):
        if byte != data1[i]:
            cutt_off = i
            break

    sample0.seek(0)
    with open('headers/header.bin', 'wb') as header:
        header.write(sample0.read(cutt_off))

    print('Wrote header file (headers/header.bin {} bytes)'.format(cutt_off))


if __name__ == '__main__':
    generate_header()

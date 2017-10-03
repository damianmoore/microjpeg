import subprocess

from PIL import Image, ImageOps
from PIL.ImageCms import profileToProfile


SRGB_PROFILE = '/usr/share/color/icc/colord/sRGB.icc'


def pil_resize(path, size):
    im = Image.open(path)
    im = ImageOps.fit(im, (size, size), Image.ANTIALIAS)
    return im


def pil_profiled_resize(path, size):
    im = Image.open(path)
    # TODO: Fix this
    # im = profileToProfile(im, SRGB_PROFILE, SRGB_PROFILE)
    # im.convert('sRGB')
    im = ImageOps.fit(im, (size, size), Image.ANTIALIAS)
    return im


def imagemagick_resize(path, size):
    '''
    Converts image in correct colorspace and gamma:
    convert in.jpg -colorspace RGB -thumbnail 32x32^ -gravity center -extent 32x32 -colorspace sRGB -quality 32 out.jpg
    '''
    cmd = [
        'convert', path,
        '-colorspace', 'RGB',
        '-thumbnail', '{0}x{0}^'.format(size),
        '-gravity', 'center',
        '-extent', '{0}x{0}'.format(size),
        '-colorspace', 'sRGB',
        '/tmp/out.png',
    ]
    subprocess.check_output(cmd)
    im = Image.open('/tmp/out.png').convert('RGB')
    return im

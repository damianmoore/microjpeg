import os
import subprocess

from PIL import Image, ImageOps
from PIL.ImageCms import profileToProfile, buildTransform, applyTransform


SRGB_PROFILE = os.path.join(os.path.dirname(__file__), '..', 'icc', 'sRGB.icc')
LINEARIZED_PROFILE = os.path.join(os.path.dirname(__file__), '..', 'icc', 'linearized-sRGB.icc')

srgb_to_linearized = buildTransform(SRGB_PROFILE, LINEARIZED_PROFILE, 'RGB', 'RGB')
linearized_to_srgb = buildTransform(LINEARIZED_PROFILE, SRGB_PROFILE, 'RGB', 'RGB')


def pil_resize(path, size):
    im = Image.open(path)
    im = ImageOps.fit(im, (size, size), Image.ANTIALIAS)
    return im


def pil_profiled_resize(path, size):
    im = Image.open(path)
    # im = profileToProfile(im, SRGB_PROFILE, LINEARIZED_PROFILE)
    im = applyTransform(im, srgb_to_linearized)
    im = ImageOps.fit(im, (size, size), Image.ANTIALIAS)
    # im = profileToProfile(im, LINEARIZED_PROFILE, SRGB_PROFILE)
    im = applyTransform(im, linearized_to_srgb)
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

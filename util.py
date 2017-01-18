import os
import random
from os.path import expanduser

scriptdir = os.path.dirname(os.path.abspath(__file__))


def prepend_proj(fname):
    """

    :param fname: Filename relative to script directory
    :return: Absolute path of file in script directory
    """
    return os.path.join(scriptdir, fname)


def prepend_home(fname):
    """

    :param fname: Filename relative to home directory
    :return: Absolute path of file in home directory
    """
    home = expanduser("~")
    return os.path.join(home, fname)


def fname_only(path):
    """
    :param path:
    :return: Filename without leading path
    """
    return path.split(os.path.sep)[-1]


def prepend_style(style_name):
    """

    :param style_name: Name of style image
    :return: Absolute path of style image file
    """
    return prepend_proj(os.path.join('style_images', style_name))


def make_input_fname():
    length = 16
    random_alphanumerical = ''.join(random.choice('0123456789ABCDEF') for _ in range(length))
    # TODO other formats than jpg?
    return prepend_proj(os.path.join('static', 'tmp-images', 'i_' + random_alphanumerical + '.jpg'))


def make_output_fname():
    length = 16
    random_alphanumerical = ''.join(random.choice('0123456789ABCDEF') for _ in range(length))
    return prepend_proj(os.path.join('static', 'tmp-images', 'o_' + random_alphanumerical + '.png'))


def output_fname(fname):
    return prepend_proj(os.path.join('static', 'tmp-images', fname))

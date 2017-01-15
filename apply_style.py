import os
from subprocess import call

import subprocess


def apply_style(content_fname, painting_fname):
    """

    :param content_fname: Picture from the user
    :param painting_fname: Painting with matching content
    :return: base_photo with the style of painting applied to it (filename)
    """

    # https://github.com/jcjohnson/neural-style

    iterations = '100'

    commands = '''cd neural-style
    /home/ubuntu/torch/install/bin/th neural_style.lua -style_image {} -content_image {} -num_iterations {}
    '''.format("~/" + painting_fname, "~/" + content_fname, iterations)

    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(commands)
    print out

    return 'neural-style/out_{}.png'.format(iterations)

import os
from subprocess import call

import subprocess

import time


def apply_style(content_fname, painting_fname):
    """

    :param content_fname: Picture from the user
    :param painting_fname: Painting with matching content
    :return: base_photo with the style of painting applied to it (filename)
    """

    # https://github.com/jcjohnson/neural-style

    start_time = time.time()

    iterations = 400

    commands = '''cd neural-style
    /home/ubuntu/torch/install/bin/th neural_style.lua -style_image {} -content_image {} -num_iterations {} -image_size 300
    '''.format("~/" + painting_fname, "~/" + content_fname, str(iterations))

    print('Executing commands: \n' + commands)

    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(commands)
    print out

    print 'apply_style after ' + str((time.time() - start_time)) + ' seconds'

    return 'neural-style/out_{}.png'.format(str(iterations - 100))

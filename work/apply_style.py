import os
from subprocess import call

from util import *
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

    iterations = 500
    image_size = 512

    output_filename = make_output_fname()
    commands = [
        'cd {}'.format(prepend_home('neural-style')),
        '/home/ubuntu/torch/install/bin/th neural_style.lua -style_image {} -content_image {} -num_iterations {} -output_image {} -image_size {}'
            .format(painting_fname, content_fname, str(iterations), output_filename, str(image_size))
    ]

    commands_str = '\n'.join(commands)

    print('Executing commands: \n' + commands_str)

    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(commands_str)
    print out

    print 'apply_style after ' + str((time.time() - start_time)) + ' seconds'

    return output_filename

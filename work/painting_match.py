import subprocess
from util import *


def match_with_painting(candidate_fname):
    """
    :param candidate_fname: Filename of picture that the client uploaded
    :return:  Filename of painting that matches the candidate photo well. None if there are no
    well-matching paintings.
    """

    commands = [
        'cd {}'.format(prepend_proj('work')),
        'python classify_image.py {}'.format(candidate_fname)
    ]

    command_str = '\n'.join(commands)

    print('Executing commands: \n' + command_str)

    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(command_str)
    print prepend_home(out)

    return out.split('\n')[-2]

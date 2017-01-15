import subprocess


def match_with_painting(candidate_fname):
    """
    :param candidate_fname: Filename of picture that the client uploaded
    :return:  Filename of painting that matches the candidate photo well. None if there are no
    well-matching paintings.
    """

    commands = '''cd backend
    python classify_image.py {}
    '''.format('~/' + candidate_fname)

    print('Executing commands: \n' + commands)

    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(commands)
    print out

    return out.split('\n')[-2]

# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Simple image classification with Inception.

Run image classification with Inception trained on ImageNet 2012 Challenge data
set.

This program creates a graph from a saved GraphDef protocol buffer,
and runs inference on an input JPEG image. It outputs human readable
strings of the top 5 predictions along with their probabilities.

Change the --image_file argument to any jpg image to compute a
classification of that image.

Please see the tutorial and website for a detailed description of how
to use this script to perform image recognition.

https://tensorflow.org/tutorials/image_recognition/
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os.path
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
import tensorflow as tf


class F:
    def __init__(self):
        self.model_dir = '/tmp/imagenet'
        self.image_file = None
        self.num_top_predictions = 5
        pass


FLAGS = F()

# pylint: disable=line-too-long
DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'


# pylint: enable=line-too-long


class NodeLookup(object):
    """Converts integer node ID's to human readable labels."""

    def __init__(self,
                 label_lookup_path=None,
                 uid_lookup_path=None):
        if not label_lookup_path:
            label_lookup_path = os.path.join(
                FLAGS.model_dir, 'imagenet_2012_challenge_label_map_proto.pbtxt')
        if not uid_lookup_path:
            uid_lookup_path = os.path.join(
                FLAGS.model_dir, 'imagenet_synset_to_human_label_map.txt')
        self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

    def load(self, label_lookup_path, uid_lookup_path):
        """Loads a human readable English name for each softmax node.

        Args:
          label_lookup_path: string UID to integer node ID.
          uid_lookup_path: string UID to human-readable string.

        Returns:
          dict from integer node ID to human-readable string.
        """
        if not tf.gfile.Exists(uid_lookup_path):
            tf.logging.fatal('File does not exist %s', uid_lookup_path)
        if not tf.gfile.Exists(label_lookup_path):
            tf.logging.fatal('File does not exist %s', label_lookup_path)

        # Loads mapping from string UID to human-readable string
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}
        p = re.compile(r'[n\d]*[ \S,]*')
        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            uid = parsed_items[0]
            human_string = parsed_items[2]
            uid_to_human[uid] = human_string

        # Loads mapping from string UID to integer node ID.
        node_id_to_uid = {}
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]

        # Loads the final mapping of integer node ID to human-readable string
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            if val not in uid_to_human:
                tf.logging.fatal('Failed to locate: %s', val)
            name = uid_to_human[val]
            node_id_to_name[key] = name

        return node_id_to_name

    def id_to_string(self, node_id):
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]


def create_graph():
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(os.path.join(
            FLAGS.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(image):
    """Runs inference on an image.

    Args:
      image: Image file name.

    Returns:
      Nothing
    """
    if not tf.gfile.Exists(image):
        tf.logging.fatal('File does not exist %s', image)
    image_data = tf.gfile.FastGFile(image, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph()

    with tf.Session() as sess:
        # Some useful tensors:
        # 'softmax:0': A tensor containing the normalized prediction across
        #   1000 labels.
        # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
        #   float description of the image.
        # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
        #   encoding of the image.
        # Runs the softmax tensor by feeding the image_data as input to the graph.
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        # Creates node ID --> English string lookup.
        node_lookup = NodeLookup()

        top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
        for node_id in top_k:
            human_string = node_lookup.id_to_string(node_id)
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))
            return get_image_name(human_string)


def maybe_download_and_extract():
    """Download and extract model tar file."""
    dest_directory = FLAGS.model_dir
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    filename = DATA_URL.split('/')[-1]
    filepath = os.path.join(dest_directory, filename)
    if not os.path.exists(filepath):
        def _progress(count, block_size, total_size):
            sys.stdout.write('\r>> Downloading %s %.1f%%' % (
                filename, float(count * block_size) / float(total_size) * 100.0))
            sys.stdout.flush()

        filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
        print()
        statinfo = os.stat(filepath)
        print('Succesfully downloaded', filename, statinfo.st_size, 'bytes.')
    tarfile.open(filepath, 'r:gz').extractall(dest_directory)


def get_image_name(subcategory):
    image_names = ['Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg',
                   'happy_birthday_miss_jones.jpg',
                   'Ultima_Cena_-_Da_Vinci_5.jpg',
                   'Meisje_met_de_parel.jpg',
                   '800px-The_Kiss.JPG',
                   '800px-The_Thinker,_Rodin.jpg',
                   '800px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg',
                   '1024px-Le_bassin_aux_nympheas_-_Claude_Monet.jpg',
                   '800px-VanGogh-self-portrait-with_bandaged_ear.jpg',
                   '800px-Wheat_stacks_in_Provence.jpg',
                   'The_Scream.jpg',
                   '800px-Auguste_Renoir_-_A_Girl_with_a_Watering_Can_-_Google_Art_Project.jpg',
                   'The-Basket-of-Apples-by-Paul-Cezanne.jpg',
                   '1024px-Michelangelo_-_Creation_of_Adam.jpg',
                   '800px-The_Kiss.JPG',
                   '1024px-Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg',
                   'The_Persistence_of_Memory.jpg']
    subcategoris = [['gown', 'stole', 'ocean', 'lake', 'cliff', 'sea', 'shore', 'coast', 'alp', 'sand'],
                    ['chair', 'table'],
                    ['dining table', 'plate', 'valley'],
                    ['lipstick'],
                    ['nipple', 'cliff dwelling', 'stone wall'],
                    ['brass', 'memorial tablet', 'plaque'],
                    ['castle', 'church', 'grocery', 'market', 'building', 'restaurant', 'thatch', 'roof', 'shop',
                     'home', 'cliff', 'tree'],
                    ['lake', 'dam', 'greenhouse'],
                    ['trench coat', 'wool', 'neck brace', 'paintbrush'],
                    ['hay', 'barn', 'patio', 'eating house', 'mortar', 'manufacture home', 'tile roof', 'lawn', 'mower',
                     'bucket', 'vase', 'jug', 'dining table', 'daisy'],
                    ['suspension bridge', 'seashore', 'sweatshirt', 'suit', 'alp', 'cliff', 'sand bar', 'face powder',
                     'lotion', 'oxygen mask', 'sunscreen'],
                    ['skirt', 'water jug', 'miniskirt', 'gown', 'velvet', 'wool', 'clog', 'greenhouse', 'patio'],
                    ['cellular telephone', 'cellular phone', 'cellphone', 'cell', 'mobile phone', 'wallet', 'billfold',
                     'notecase', 'pocketbook'],
                    ['pedestal', 'throne', 'studio', 'couch', 'day bed', 'altar', 'church', 'building',
                     'cliff dwelling', 'dome', 'stone wall', 'diaper', 'sarong', 'cloak'],
                    ['daisy', 'quilt', 'conforter', 'sleeping bag'],
                    ['daisy', 'wing', 'pier', 'lakeside', 'lakeshore', 'sandbar', 'sand bar', 'gown', 'stole', 'cloak',
                     'chiton'], ['clock']]

    for i in range(len(subcategoris)):
        for j in range(len(subcategoris[i])):
            if subcategoris[i][j].lower() in subcategory.lower():
                return image_names[i];

    return image_names[len(image_names) - 1]


def main():
    maybe_download_and_extract()
    image = (FLAGS.image_file if FLAGS.image_file else
             os.path.join(FLAGS.model_dir, 'cropped_panda.jpg'))
    print(image)
    print(run_inference_on_image(image))


def run(main=None, argv=None):
    """Runs the program with an optional 'main' function and 'argv' list."""

    from tensorflow.python.platform import flags

    f = flags.FLAGS

    # Extract the args from the optional `argv` list.
    args = argv[1:] if argv else None

    # Parse the known flags from that list, or from the command
    # line otherwise.
    # pylint: disable=protected-access
    flags_passthrough = f._parse_flags()
    # pylint: enable=protected-access

    main = main or sys.modules['__main__'].main

    # Call the main function, passing through any arguments
    # to the final program.
    sys.exit(main())


def match_with_painting(candidate_fname):
    """
    :param candidate_fname: Filename of picture that the client uploaded
    :return:  Filename of painting that matches the candidate photo well. None if there are no
    well-matching paintings.
    """

    FLAGS.image_file = candidate_fname

    # replaces tf.app.run()
    return run(main=main, argv=[sys.argv[0]])

    # return 'neural-style/sample_style.jpg'


# print(match_with_painting('/Users/abureyanahmed/Downloads/suit.jpeg'))

# print(get_image_name('eating house'))


if __name__ == '__main__':
    match_with_painting(sys.argv[1])

import subprocess
from util import *


def match_with_painting(candidate_fname):
    """
    :param candidate_fname: Filename of picture that the client uploaded
    :return:  Filename of painting that matches the candidate photo well. None if there are no
    well-matching paintings.
    """

    image_names = ['mona_lisa.jpg',
                   'happy_birthday_miss_jones.jpg',
                   'ultima_cena.jpg',
                   'met_de_parel.jpg',
                   'starry_night.jpg',
                   'le_bassin_aux_nympheas.jpg',
                   'van_gogh_self_portrait.jpg',
                   'wheat_stacks_in_provence.jpg',
                   'the_scream.jpg',
                   'a_girl_with_a_watering_can.jpg',
                   'basket_of_apples.jpg',
                   'creation_of_adam.jpg',
                   'the_persistence_of_memory.jpg',
                   'twelve_sunflowers.jpg',
                   'sunday_on_la_grande_jatte.jpg',
                   'american_gothic.jpg',
                   'luncheon_of_the_boating_party.jpg',
                   'tsunami.jpg',
                   'singing_butler.jpg']

    return image_names[random.randint(0, len(image_names) - 1)]

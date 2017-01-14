from subprocess import call


def apply_style(content_photo, painting):
    """

    :param content_photo: Picture from the user
    :param painting: Painting with matching content
    :return: base_photo with the style of painting applied to it
    """

    # https://github.com/jcjohnson/neural-style
    # th neural_style.lua -style_image <image.jpg> -content_image <image.jpg>
    # call(["th", "neural_style.lua", "-style_image", image_path, "-content_image", content_path])
    # saved to out.png

    return None
from PIL import Image
import flask
from flask import Flask
from flask import send_file
from io import BytesIO

import apply_style
import painting_match
import push_device

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Use the /upload to upload mutiple images!'


@app.route("/upload", methods=["POST"])
def upload():
    content_fname = 'tmp-images/content_image.jpg'
    flask.request.files['uploadedfile1'].save(content_fname)
    # resize(content_fname)

    fcm_token = flask.request.headers['fcm-token']

    painting = painting_match.match_with_painting(content_fname)

    print('Painting: ' + painting)

    painting = 'backend/style_images/' + painting

    if painting is not None:
        result = apply_style.apply_style(content_fname, painting)

        # client request probably timed out by now
        push_device.notify_device(fcm_token, result)
        return "Rendered successfully"
    else:
        return "No matching paintings"


def resize(fname):
    im = Image.open(fname)
    im.thumbnail([300, 300], Image.ANTIALIAS)
    # imResize = im.resize((400,400), Image.ANTIALIAS)
    im.save(fname, 'JPEG', quality=90)


def serve_image(filename):
    return send_file(filename, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

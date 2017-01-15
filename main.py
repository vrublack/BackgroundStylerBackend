import flask
from flask import Flask
from flask import send_file
from io import BytesIO

import apply_style
import painting_match

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Use the /upload to upload mutiple images!'


@app.route("/upload", methods=["POST"])
def upload():
    content_fname = 'tmp-images/content_image.jpg'
    flask.request.files['uploadedfile1'].save(content_fname)

    painting = painting_match.match_with_painting(content_fname)

    if painting is not None:
        result = apply_style.apply_style(content_fname, painting)
        return serve_image(result)
    else:
        return "No matching paintings"


def serve_image(filename):
    return send_file(filename, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

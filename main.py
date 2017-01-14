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

    photo, painting = painting_match.match_with_painting(content_fname)

    if painting is not None:
        result = apply_style.apply_style(photo, painting)
        return serve_image(result)
    else:
        return "No matching paintings"


def serve_image(img):
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

from work.apply_style import apply_style
import flask
from PIL import Image
from celery import Celery
from flask import Flask
from flask import send_file

import push_device
from util import *
from work import painting_match

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task(name='process_image')
def process_image(content_fname, fcm_token):
    """
    Runs in the background to process the image
    :param content_fname:
    :param fcm_token:
    :return:
    """
    painting = painting_match.match_with_painting(content_fname)

    print('Painting: ' + painting)

    painting = prepend_style(painting)

    if painting is not None:
        result = apply_style(content_fname, painting)
        result = fname_only(result)
        # client notified and provided with the filename
        push_device.notify_device(fcm_token, result, painting)
    else:
        # client not notified, nothing happens
        pass


@app.route('/')
def hello_world():
    return 'Use the /upload to upload mutiple images!'


@app.route("/upload", methods=["POST"])
def upload():
    content_fname = make_input_fname()
    flask.request.files['uploadedfile1'].save(content_fname)
    fcm_token = flask.request.headers['fcm-token']

    process_image.delay(content_fname, fcm_token)

    return "Processing image..."


def resize(fname):
    im = Image.open(fname)
    im.thumbnail([300, 300], Image.ANTIALIAS)
    # imResize = im.resize((400,400), Image.ANTIALIAS)
    im.save(fname, 'JPEG', quality=90)


def serve_image(filename):
    return send_file(filename, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

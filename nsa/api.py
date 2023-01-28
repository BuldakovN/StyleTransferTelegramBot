import flask
from model import run1, run2
import os, io
import torch
from PIL import Image
import torch
from torchvision.transforms.functional import to_pil_image

app = flask.Flask(__name__)

@app.route('/')
def index():
    return 'Отправьте изображение в POST-запросе на /sendimage'


@app.route('/sendimage1', methods=['POST'])
def sendimage1():
    # получить изображение
    content_image = flask.request.files['content_image']
    # преобразовать в PIL
    content_image = Image.open(content_image)
    # преобразуем PIL в тензор
    output_image = run1(content_image)
    output_image = to_pil_image(output_image)
    # возвращает изображение
    output_img_io = io.BytesIO()
    output_image.save(output_img_io, 'PNG')
    output_img_io.seek(0)
    return flask.send_file(output_img_io, mimetype='image')


@app.route('/sendimage2', methods=['POST'])
def sendimage2():
    # получить изображение
    content_image = flask.request.files['content_image']
    style_image = flask.request.files['style_image']
    # преобразовать в PIL
    content_image = Image.open(content_image)
    style_image = Image.open(style_image)
    # преобразуем PIL в тензор
    output_image = run2(content_image, style_image)
    output_image = to_pil_image(output_image)
    # возвращает изображение
    output_img_io = io.BytesIO()
    output_image.save(output_img_io, 'PNG')
    output_img_io.seek(0)
    return flask.send_file(output_img_io, mimetype='image')

if __name__ == '__main__':
    print('Start API')
    app.run(host='0.0.0.0', port='1337', debug=True)
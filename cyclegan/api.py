import flask
from model import CycleNet, pil_to_tensor
import os, io
import torch
from PIL import Image
import torch
from torchvision.transforms.functional import to_pil_image

model = CycleNet()
cur_dir = os.path.dirname(os.path.realpath(__file__))
model.load_state_dict(torch.load(cur_dir+'/G_AB.pth', map_location=torch.device('cpu')))
model.eval()

app = flask.Flask(__name__)

def tensor_to_pil(tensor):
    tensor = (tensor+1)/2
    tensor = tensor.clone().detach().cpu()
    img = to_pil_image(tensor)
    return img


@app.route('/sendimage', methods=['POST'])
def sendimage():
    # получить изображение
    image = flask.request.files['content_image']
    # преобразовать в PIL
    image = Image.open(image)
    # преобразуем PIL в тензор
    image = pil_to_tensor(image, 'cpu')
    image = model(image.unsqueeze(0)).squeeze(0)
    image = tensor_to_pil(image)
    # возвращает изображение
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return flask.send_file(img_io, mimetype='image')

if __name__ == '__main__':
    print('Start API')
    app.run(host='0.0.0.0', port='1707', debug=True)
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import json
import io, os
from PIL import Image
from requests import post
import torch
from torchvision.transforms.functional import to_pil_image
from torchvision.utils import save_image

from msg import model as msg
from cyclegan import model as cyclegan
from nsa import model as nsa

cur_dir = os.path.dirname(os.path.realpath(__file__))
with open(cur_dir+'/config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)
with open(cur_dir+'/TOKEN', 'r') as f:
    TOKEN = f.read().replace('\n', '')

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(CONFIG['greetings'])


"""Попытка сделать микросервисную архитектуру
@dp.message_handler(lambda message: message.caption == '/cyclegan', content_types=ContentType.ANY)
async def cyclegan(message: types.Message):
    print('cyclegan')
    lines = CONFIG['cyclegan']
    image = io.BytesIO()
    image = await message.photo[-1].download(destination_file=image)
    await message.reply(lines['start'])
    try:
        image = post(lines['url']+':1707/sendimage', files={'content_image':image})
    except:
        await message.reply(lines['error'])
        return
    if not image.ok:
        await message.reply(lines['error'])
        return
    image = Image.open(io.BytesIO(image.content))
    
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image = output.getvalue()

    await message.reply_photo(image, caption=lines['success'])


@dp.message_handler(lambda message: message.caption == '/msg1', content_types=ContentType.ANY)
async def msg1(message: types.Message):
    print('msg1')
    lines = CONFIG['msg']
    image = io.BytesIO()
    image = await message.photo[-1].download(destination_file=image)
    await message.reply(lines['start'])
    try:
        image = post(lines['url']+':1202/sendimage1', files={'content_image':image})
    except:
        await message.reply(lines['error'])
        return
    if not image.ok:
        await message.reply(lines['error'])
        return
    image = Image.open(io.BytesIO(image.content))
    
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image = output.getvalue()
    await message.reply_photo(image, caption=lines['success'])


@dp.message_handler(lambda message: message.caption == '/msg2', content_types=ContentType.ANY)
async def msg2(message: types.Message):
    print('msg2')
    lines = CONFIG['msg']
    content_image = io.BytesIO()
    content_image = await message.photo[0].download(destination_file=content_image)
    style_image = io.BytesIO()
    style_image = await message.photo[-1].download(destination_file=style_image)
    await message.reply(lines['start'])
    try:
        image = post(lines['url']+':1202/sendimage2', files={'content_image':content_image, 'style_image':style_image})
    except:
        await message.reply(lines['error'])
        return
    if not image.ok:
        await message.reply(lines['error'])
        return
    image = Image.open(io.BytesIO(image.content))
    
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image = output.getvalue()
    await message.reply_photo(image, caption=lines['success'])


@dp.message_handler(lambda message: message.caption == '/nsa1', content_types=ContentType.ANY)
async def nsa1(message: types.Message):
    print('nsa1')
    lines = CONFIG['nsa']
    image = io.BytesIO()
    image = await message.photo[-1].download(destination_file=image)
    await message.reply(lines['start'])
    try:
        image = post(lines['url']+':1337/sendimage1', files={'content_image':image})
    except:
        await message.reply(lines['error'])
        return
    if not image.ok:
        await message.reply(lines['error'])
        return
    image = Image.open(io.BytesIO(image.content))
    
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image = output.getvalue()

    await message.reply_photo(image, caption=lines['success'])"""


def tensor_to_pil(tensor):
    tensor = (tensor+1)/2
    tensor = tensor.clone().detach().cpu()
    img = to_pil_image(tensor)
    return img

@dp.message_handler(lambda message: message.caption == '/cyclegan', content_types=ContentType.ANY)
async def cyclegan_handler(message: types.Message):
    print('cyclegan')
    model = cyclegan.CycleNet()
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    model.load_state_dict(torch.load(cur_dir+'/cyclegan/G_AB.pth', map_location=torch.device('cpu')))
    lines = CONFIG['cyclegan']
    image = io.BytesIO()
    image = await message.photo[-1].download(destination_file=image)
    await message.reply(lines['start'])
    try:
        image = Image.open(image)
        image = cyclegan.pil_to_tensor(image, 'cpu')
        image = model(image.unsqueeze(0)).squeeze(0)
        image = tensor_to_pil(image)
    except Exception as e:
        print(e)
        await message.reply(lines['error'])
        return
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image = output.getvalue()

    await message.reply_photo(image, caption=lines['success'])


@dp.message_handler(lambda message: message.caption == '/msg1', content_types=ContentType.ANY)
async def msg1_handler(message: types.Message):
    print('msg1')
    lines = CONFIG['msg']
    image = io.BytesIO()
    image = await message.photo[-1].download(destination_file=image)
    await message.reply(lines['start'])
    try:
        image = Image.open(image)
        image = msg.run1(image)
    except Exception as e:
        print(e)
        await message.reply(lines['error'])
        return
 
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image = output.getvalue()
    await message.reply_photo(image, caption=lines['success'])


@dp.message_handler(lambda message: message.caption == '/nsa1', content_types=ContentType.ANY)
async def nsa1_handler(message: types.Message):
    print('nsa1')
    lines = CONFIG['nsa']
    image = io.BytesIO()
    image = await message.photo[-1].download(destination_file=image)
    await message.reply(lines['start'])
    try:
        # преобразовать в PIL
        image = Image.open(image)
        # преобразуем PIL в тензор
        image = nsa.run1(image)
        image = to_pil_image(image)
    except Exception as e:
        print(e)
        await message.reply(lines['error'])
        return    
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image = output.getvalue()
    await message.reply_photo(image, caption=lines['success'])


def run():
    print('start')
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    run()
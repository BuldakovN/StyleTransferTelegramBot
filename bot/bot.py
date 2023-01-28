from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import json
import torch
import base64, io, os
from PIL import Image
from requests import post

cur_dir = os.path.dirname(os.path.realpath(__file__))
with open(cur_dir+'/config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)
#API_TOKEN = config['token']
with open(cur_dir+'/TOKEN', 'r') as f:
    TOKEN = f.read()

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(CONFIG['greetings'])


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

    await message.reply_photo(image, caption=lines['success'])


if __name__ == '__main__':
    print('start')
    executor.start_polling(dp, skip_updates=True)
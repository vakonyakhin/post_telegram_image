from datetime import date, timedelta
import requests
import os
import time
import random

import telegram
from telegram.ext import Updater, Dispatcher, MessageHandler, CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters


def start(update, context):
    update.message.reply_text(
        'Поехали. Буду присылать по одной фотографии каждый день.'
    )


def text(update, context):
    update.message.reply_text(
        'Я не понимаю текст и не веду беседу. Завтра будет новое фото.'
    )


def download_image(url, name, directory='images/'):
    response = requests.get(url)
    response.raise_for_status

    image = f'{directory}{name}'
    if not os.path.exists(image):
        with open(f'{directory}{name}', 'wb') as image:
            image.write(response.content)


def get_nasa_images(url, key):
    delta = 30
    time_delta = timedelta(days=delta)
    params = {
        'api_key': key,
        'start_date': date.today() - time_delta,
        'end_date': date.today(),
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    nasa_content = response.json()
    return nasa_content


def find_image(directory='images/'):
    images = os.listdir(directory)

    for image_num, image in enumerate(images):
        with open(directory + image, 'rb') as image:
            return image.read()


def post_image(update, chat_id, image):
    update.bot.send_photo(chat_id, image)


def main():

    chat_id = os.getenv('CHAT_ID')
    tg_token = os.getenv('TG_KEY')

    nasa_key = os.getenv('NASA_API_KEY')
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    name_nasa = '_nasa.jpg'

    name_spacex = '_spaceX.jpg'
    launch_spacex = random.randint(1, 100)
    spacex_url = f'https://api.spacexdata.com/v3/launches/{launch_spacex}'
    directory = 'images/'

    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text))

    if not os.path.exists(directory):
        os.mkdir(directory)

    nasa_content = get_nasa_images(nasa_url, nasa_key)
    for image in nasa_content:
        download_image(image['url'], f'{image["date"]}{name_nasa}')

    while True:
        image = find_image()
        post_image(updater, chat_id, image)
        time.sleep(10)


if __name__ == '__main__':
    main()
from datetime import date, timedelta
import requests
import os
import time
import random

import telegram
from telegram.ext import Updater, Dispatcher, MessageHandler, CommandHandler
from telegram.ext import Filters
from dotenv import load_dotenv


def start(update, context):
    update.message.reply_text(
        'Поехали. Буду присылать по одной фотографии каждый день.'
    )


def return_text(update, context):
    update.message.reply_text(
        'Я не понимаю текст и не веду беседу. Завтра будет новое фото.'
    )


def download_image(url, name, directory='images/'):
    response = requests.get(url)
    response.raise_for_status

    image_path = f'{directory}{name}'

    with open(image_path, 'wb') as image:
        image.write(response.content)


def get_nasa_api_content(url, api_key, prefix='nasa_', format='.jpg'):
    delta = 30
    time_delta = timedelta(days=delta)
    params = {
        'api_key': api_key,
        'start_date': date.today() - time_delta,
        'end_date': date.today(),
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    nasa_content = response.json()

    for image in nasa_content:
        if image['media_type'] == 'image':
            download_image(image['url'], f'{prefix}{image["date"]}{format}')


def get_spacex_api_content(url, image_prefix='spacex', file_format='.jpg'):
    response = requests.get(url)
    response.raise_for_status()

    image_urls = response.json()['links']['flickr_images']

    for url_count, url in enumerate(image_urls):
            download_image(url, f'{image_prefix}{url_count}{file_format}')


def start_tg_settings(token):
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, return_text))

    return updater


def post_images(updater, chat_id, directory='images/'):
    images = os.listdir(directory)
    while True:
        for image in images:
            with open(f'{directory}{image}', 'rb') as posted_image:
                updater.bot.send_photo(chat_id, posted_image)
            time.sleep(86400)


def main():
    load_dotenv()
    tg_chat_id = os.getenv('TG_CHAT_ID')
    tg_token = os.getenv('TG_KEY')

    nasa_key = os.getenv('NASA_API_KEY')
    nasa_url = 'https://api.nasa.gov/planetary/apod'

    launch_number = random.randint(1, 100)
    spacex_url = f'https://api.spacexdata.com/v3/launches/{launch_number}'

    directory = 'images/'

    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, return_text))

    os.makedirs(directory, exist_ok=True)

    updater = start_tg_settings(tg_token)

    get_nasa_api_content(nasa_url, nasa_key)
    get_spacex_api_content(spacex_url)

    post_images(updater, tg_chat_id)


if __name__ == '__main__':
  main()
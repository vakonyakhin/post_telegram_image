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


def fetch_nasa_images(url, api_key, directory):
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
            response = requests.get(image['url'])
            response.raise_for_status()
            file_format = os.path.splitext(image['url'])
            print(file_format)
            image_path = f'{directory}nasa_{image["date"]}{file_format[1]}'

            with open(image_path, 'wb') as image:
                image.write(response.content)


def fetch_spacex_launnch_images(url, directory, file_format='.jpg'):
    response = requests.get(url)
    response.raise_for_status()

    image_urls = response.json()['links']['flickr_images']

    for url_count, url in enumerate(image_urls):
        response = requests.get(url)
        response.raise_for_status()

        image_path = f'{directory}spacex{url_count}{file_format}'

        with open(image_path, 'wb') as image:
            image.write(response.content)


def setup_tg_bot(token):
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

    os.makedirs(directory, exist_ok=True)

    updater = setup_tg_bot(tg_token)

    fetch_nasa_images(nasa_url, nasa_key, directory)
    fetch_spacex_launnch_images(spacex_url, directory)

    post_images(updater, tg_chat_id)


if __name__ == '__main__':
    main()
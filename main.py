from datetime import date, timedelta
import requests
import os
import time
import random
from urllib.parse import urlparse, unquote

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


def download_image(url, name, path):
    response = requests.get(url)
    response.raise_for_status()
    file_format = get_file_extention(url)
    image_path = f'{path}{name}{file_format}'
    with open(image_path, 'wb') as image:
        image.write(response.content)


def get_file_extention(url):
    url_parse = urlparse(url)
    file_name = unquote(os.path.split(url_parse.path)[1])
    file_extention = os.path.splitext(file_name)[1]
    return file_extention


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
            download_image(image['url'], f'nasa_{image["date"]}', directory)


def fetch_spacex_launch_images(url, directory):
    response = requests.get(url)
    response.raise_for_status()

    image_urls = response.json()['links']['flickr_images']

    for url_count, url in enumerate(image_urls):
        download_image(url, f'spacex{url_count}', directory)


def setup_tg_bot(token):
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, return_text))

    return updater


def post_images(updater, chat_id, directory):
    images = os.listdir(directory)
    while True:
        for image in images:
            with open(f'{directory}{image}', 'rb') as being_sent_image:
                updater.bot.send_photo(chat_id, being_sent_image)
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
    fetch_spacex_launch_images(spacex_url, directory)
    post_images(updater, tg_chat_id, directory)


if __name__ == '__main__':
    main()

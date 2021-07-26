from datetime import date, timedelta
import requests
import os
import time
import random

import telegram
from telegram.ext import Updater, Dispatcher, MessageHandler, CommandHandler
from telegram.ext import CallbackContext
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


def get_nasa_api_content(url, api_key):
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


def get_spacex_api_content(url):
    response = requests.get(url)
    response.raise_for_status()

    image_urls = response.json()['links']['flickr_images']

    return image_urls


def find_image(directory='images/'):
    images = os.listdir(directory)

    for image in images:
        yield image


def post_image(update, chat_id, image):
    update.bot.send_photo(chat_id, image)


def main():
    load_dotenv()
    chat_id = os.getenv('CHAT_ID')
    tg_token = os.getenv('TG_KEY')

    nasa_key = os.getenv('NASA_API_KEY')
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    
    launch_spacex = random.randint(1, 100)
    spacex_url = f'https://api.spacexdata.com/v3/launches/{launch_spacex}'
    
    directory = 'images/'
    name_nasa = 'nasa_'
    name_spacex = 'spaceX'
    format_file = '.jpg'

    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, return_text))
    

    if not os.path.exists(directory):
        os.mkdir(directory)

    nasa_content = get_nasa_api_content(nasa_url, nasa_key)
     
    for image in nasa_content:
        if image['media_type'] == 'image':
            download_image(image['url'], f'{name_nasa}{image["date"]}{format_file}')

    spacex_content = get_spacex_api_content(spacex_url)
    if spacex_content:
        for num_url, url in enumerate(spacex_content):
            download_image(url, f'{name_spacex}{num_url}{format_file}')

    images = find_image()
    while True:
        try:
            image = next(images)
            with open(f'{directory}{image}', 'rb') as posted_image:
                post_image(updater, chat_id, posted_image)
            time.sleep(86400)
        except StopIteration:
            updater.bot.send_message(chat_id, 'Фоток больше нет')
            break


if __name__ == '__main__':
    main()
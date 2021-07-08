from datetime import date
import requests
import os
import time

import telegram
from telegram.ext import Updater, Dispatcher, MessageHandler, CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters

def start(update, context):
    update.message.reply_text('Поехали. Буду присылать по одной фотографии каждый день')
    

def text(update, context):
  update.message.reply_text('Я не понимаю текст и не веду беседу. Завтра будет новое фото дня от NASA')


def get_nasa_foto(url, key):
  params = {
      'api_key': key,
      'date': date.today(),
  }
  response = requests.get(url, params=params)
  response.raise_for_status()

  return response.json()['url']


def post_image(update,chat_id, photo):
    update.bot.send_photo(chat_id, photo)


def main():
    chat_id = os.getenv('CHAT_ID')
    tg_token = os.getenv('TG_KEY')
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    nasa_key = os.getenv('NASA_API_KEY')
    updater = Updater(tg_token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text))

    image = get_nasa_foto(nasa_url, nasa_key)
    
    post_image(updater,chat_id, image)
    
 
if __name__ == '__main__':
  while True:
    main()
    time.sleep(86400)







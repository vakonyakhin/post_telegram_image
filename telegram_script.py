import os

import telegram
from telegram.ext import Updater, Dispatcher, MessageHandler, CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters



        


    

def create_bot():
    
    token = os.getenv('TG_CHAT_ID')
    bot = telegram.Bot(token)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))   

    return bot
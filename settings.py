import os

from dotenv import load_dotenv

from aiogram import Bot
from aiogram import Dispatcher

# load_dotenv() we use it to deliver our token from the .env file
load_dotenv()

# define the bot variable in which we call the bot and pass the token to it
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

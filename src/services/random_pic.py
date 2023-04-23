import os

import requests

from dotenv import load_dotenv

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import types, Router
from aiogram.filters import Text

from static.start import commands


# All handlers should be attached to the Router (or Dispatcher) need for correct routing work
random_pic_router = Router()

# load_dotenv() we use it to deliver our token from the .env file
load_dotenv()


# Here we create a class and inherit from the base class StatesGroup to store our answers in memory
class Random(StatesGroup):
    func = State()


# In @random_pic_router.message decorator, we use the standard Text filter
# from the aiogram library so that the bot has a reaction
# to pressing a button that contains text in {bots_func[2]}


@random_pic_router.message(Text(f"{commands[2]}"))
async def get_cuties(message: types.Message, state: FSMContext):
    """

    :param message: a message from user
    :param state: in order for us to be able to write user data to memory
    :return: answer from bot with random photo of animal and photo description

    """

    # Here we take the token received by c https://unsplash.com/developers
    token = os.getenv('UNSPLASH_TOKEN')
    # Here we define an url variable that stores the address with random photos
    url = f"https://api.unsplash.com/photos/random?collections=4760062&client_id={token}"
    # In the response variable we store a GET request to which we pass our url
    response = requests.request("GET", url)
    # In the result variable we store the parsed link, that returns JSON
    result = response.json()
    # From the variables description and random photo,
    # we get information on the keys from the response contained in the result variable
    description = result['alt_description']
    random_photo = result['links']['download']
    # And here is our :return: with random photo of animal and photo description
    await state.set_state(Random.func)
    await message.answer_photo(photo=random_photo, caption=description)
    # here we set the state
    # exiting the state
    await state.clear()

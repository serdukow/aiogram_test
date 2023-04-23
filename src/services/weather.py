import os

import emoji

import requests
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv

from aiogram.filters import Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types, Router
from aiogram.fsm.state import State, StatesGroup

from static.weather import weather_conditions
from static.start import commands


# All handlers should be attached to the Router (or Dispatcher) need for correct work routing
weather_router = Router()


# load_dotenv() we use it to deliver our token from the .env file
load_dotenv()


# Here we create a class and inherit from the base class StatesGroup to store our answers in memory
class Weather(StatesGroup):
    func = State()


# In @weather_router.message decorator, we use the standard Text filter
# from the aiogram library so that the bot has a reaction
# to pressing a button that contains text in {bots_func[0]}


@weather_router.message(Text(f"{commands[0]}"))
async def weather_command(message: types.Message, state: FSMContext):

    """
    :param message: a message from user
    :param state: in order for us to be able to write user data to memory
    :return: returns a message asking you to enter the name of the city

    """

    # In the builder variable, we store the keyboard call and then
    # add the "Return to main menu" button
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Back to main menu'))
    # resize_keyboard is the param which make our keyboard smaller
    await message.answer(f"Enter the name of the city {emoji.emojize(':backhand_index_pointing_down:')}",
                         reply_markup=builder.as_markup(resize_keyboard=True))
    # here we set the state
    await state.set_state(Weather.func)


# Here is our func, which shows a weather in city you enter
# also a decorator to link the func to our command above

# And here we have a handler that will respond only to this condition 'Weather.state'
@weather_router.message(Weather.func)
async def get_weather(message: types.Message, state: FSMContext):

    """

    :param message: a message from user
    :param state: in order for us to be able to write user data to memory
    :return: returns a message answer with current weather and other info

    """

    # Here our token from .env
    open_weather_token = os.getenv('OW_TOKEN')
    # In the weather_data variable, we store explanations for each key
    # in our response in order for the answers to be with emojis
    weather_data = weather_conditions
    # In this function, we use the try except construct to handle an error
    # if it is, for example, an incorrectly entered city or KeyError
    try:
        # In the response variable we store a GET request to which we pass our url
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q="
            f"{message.text}&appid={open_weather_token}&units=metric"
        )
        # In the result variable we store the parsed link, that returns JSON
        result = response.json()
        # From the variables city and random current_weather,
        # we get information on the keys from the response contained in the result variable,
        # its name of the city contains in "name" and current weather of this city
        city = result["name"]
        current_weather = round(result["main"]["temp"])
        # in the variable weather_description we store the result of receiving data from our request
        # by keys we pull our information with a description of the weather
        weather_description = result["weather"][0]["main"]
        # then we process the error in case there is no information and output a message
        # "Better take a look out the window, I missed something"
        if weather_description in weather_data:
            wd = weather_data[weather_description]
        else:
            wd = f"Better take a look out the window, " \
                 f"I missed something {emoji.emojize(':window:')}"
        # The variables fells_like, humidity, pressure and wind store the relevant weather information,
        # which we collect by keys
        feels_like = round(result["main"]["feels_like"])
        humidity = result["main"]["humidity"]
        pressure = result["main"]["pressure"]
        wind = result["wind"]["speed"]
        # And here is our :await: with answer about weather in city which we are enter
        await message.answer(
                    f"It's {current_weather}C° in {city} now\n"
                    f"Feels like {feels_like}C°\n"
                    f"{wd}\n"
                    f"Humidity is: {humidity}%\n"
                    f"Pressure is: {pressure} mmHg\n"
                    f"Wind is: {wind} mps\n"
            )
    # Here we handle the ValueError and if it returned  message to user
    # 'Something went wrong. Let me deal.'
    except ValueError:
        await message.answer('Something went wrong. Let me deal.')
    # And finally, if the user clicks on the 'Back to main menu' button,
    # we reply that 'You are returned to the main menu'
    finally:
        if message.text == 'Back to main menu':
            # In the builder variable, we store the keyboard call and then
            # add the "Return to main menu" button
            builder = ReplyKeyboardBuilder()
            for i in commands:
                builder.row(types.KeyboardButton(text=str(i)))
            builder.row()
            await message.answer(text='You are returned to the main menu',
                                 reply_markup=builder.as_markup(resize_keyboard=True))
            # exiting the state
            await state.clear()

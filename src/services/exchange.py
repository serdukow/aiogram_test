import os

import requests

from dotenv import load_dotenv

import emoji

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types, Router


from static.start import commands

# All handlers should be attached to the Router (or Dispatcher) need for correct routing work
exchange_router = Router()

# load_dotenv() we use it to deliver our token from the .env file
load_dotenv()


# Here we create a class and inherit from the base class StatesGroup to store our answers in memory
class Exchange(StatesGroup):
    func = State()

# In @exchange_router.message decorator, we use the standard Text filter
# from the aiogram library so that the bot has a reaction
# to pressing a button that contains text in {bots_func[1]}


@exchange_router.message(Text(f"{commands[1]}"))
async def exchange(message: types.Message, state: FSMContext):

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
    await message.answer(f"Convert any currency in formate like this "
                         f"EUR to RUB 100 {emoji.emojize(':backhand_index_pointing_down:')}",
                         reply_markup=builder.as_markup(resize_keyboard=True))
    # here we set the state
    await state.set_state(Exchange.func)


# here we have a handler that will respond only to this condition 'Exchange.state'
@exchange_router.message(Exchange.func)
async def get_currency(message: types.Message, state: FSMContext):

    """
    :param message: waiting a message from user in format like 'RUB to EUR 1000'
    :param state: in order for us to be able to write user data to memory
    :return: returns a message answer with converted currency

    """

    # Here our token from .env
    token = os.getenv('NINJA_TOKEN')
    # Here is our url that we changed so that the values that the user entered would be put under the url
    url = f'https://api.api-ninjas.com/v1/convertcurrency?want={message.text.split()[0]}' \
          f'&have={message.text.split()[2]}&amount={message.text.split()[3]}'
    # In the response variable we store a GET request and param with token which we pass our url
    response = requests.get(url, headers={'X-Api-Key': f'{token}'})
    # In the result variable we store the parsed link, that returns JSON
    result = response.json()
    # Next, we have a condition that the currencies are bigger than 3 char and amount is bigger or equals 1,
    # if they are not, then the message '...Cant find...' is displayed
    if len(message.text.split()[0]) and len(message.text.split()[2]) == 3 and len(message.text.split()[3]) >= 1:
        amount = result['new_amount']
        await message.answer(f'{amount} {message.text.split()[0]}')
    elif message.text == 'Back to main menu':
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
    else:
        await message.answer(f'Cant find {message.text.split()[0]} and {message.text.split()[2]} in currencies data\n'
                             f'Also note, that amount must be bigger than 0.')


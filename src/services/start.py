from aiogram import types, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from static.start import greeting, friends_gif, commands

start_router = Router()

# Here we process the start command, when clicked, the user sees a message with buttons
# that are contained in bots_func and a gif that is contained in the gif variable


@start_router.message(Command(commands=['start', 'help']))
async def start_command(message: types.Message):
    # In the builder variable, we store the keyboard call and then
    builder = ReplyKeyboardBuilder()
    # Here we cycle through commands and output the information to the buttons
    for i in commands:
        builder.row(types.KeyboardButton(text=str(i)))
    builder.row()
    gif = f'{friends_gif}'
    caption = f'{greeting}'
    # output message with the buttons
    await message.answer_animation(animation=gif, caption=caption,
                                   reply_markup=builder.as_markup(resize_keyboard=True))

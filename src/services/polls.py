import emoji

from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods import SendPoll
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ReplyKeyboardRemove

from static.start import commands
from static.polls import polls_options_note

# All handlers should be attached to the Router (or Dispatcher) need for correct routing work
polls_router = Router()


# Here we create a class and inherit from the base class StatesGroup to store our answers in memory
class Polls(StatesGroup):
    question = State()
    answer = State()

# In @polls_router.message decorator, we use the standard Text filter
# from the aiogram library so that the bot has a reaction
# to pressing a button that contains text in {bots_func[3]}


@polls_router.message(Text(f"{commands[3]}"))
async def poll_command(message: types.Message, state: FSMContext):

    """

    :param message: a message from user
    :param state: in order for us to be able to write user data to memory
    :return: User create poll and send it to your group

    """

    # here we send a message to the user and ask him to write a question
    # and at the same time we remove the keyboard with ReplyKeyboardRemove()
    await message.answer(f"Choose a question you want to publish {emoji.emojize(':backhand_index_pointing_down:')}\n\n"
                         f"{polls_options_note}",
                         reply_markup=ReplyKeyboardRemove())
    # here we set the state
    await state.set_state(Polls.question)


# here we have a handler that will respond only to this condition 'Polls.questions'
@polls_router.message(Polls.question)
async def question_chosen(message: types.Message, state: FSMContext):
    # here we update the data in the state and bring them in chosen_question
    await state.update_data(chosen_question=message.text)
    # here we send a message to the user and ask him to choose options
    await message.answer(
        f"Choose the answer options {emoji.emojize(':backhand_index_pointing_down:')}")
    # here we set the state
    await state.set_state(Polls.answer)


# here we have a handler that will respond only to this condition 'Polls.answer'
@polls_router.message(Polls.answer)
async def question_chosen(message: types.Message, state: FSMContext):
    # In this function, we use the try except construct to handle an error
    # if it is, for example, an incorrectly entered answers or TelegramBadRequest
    # and we output an error message
    try:
        # here we update the data in the state and bring them in chosen_answers
        # separated by comma
        await state.update_data(chosen_answers=message.text.split(', '))
        # catch the data that we received from the previous answers
        user_data = await state.get_data()
        # divide them by variables
        question = user_data['chosen_question']
        answers = user_data['chosen_answers']
        # if answers bigger or equal 2 we send poll to group
        # but if less user receive message with error
        if len(answers) >= 2:
            await SendPoll(chat_id='-833156326', question=question, options=list(answers))
            # here we clear the state
            await state.clear()
        else:
            await message.answer("Poll must have at least 2 option. Try again.")
    except TelegramBadRequest:
        await message.answer("Poll can't have more than 10 options. Try again.")

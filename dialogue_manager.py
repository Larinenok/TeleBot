import asyncio
from random import randint
from auth_data import bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram.utils.callback_data import CallbackData
from json_reader import load_message_by_id


bot = Bot(bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def view_message(message: types.Message, message_id: str):
    quest_message = load_message_by_id(message_id)
    buttons = []
    for i in quest_message.Answers:
        buttons.append(types.InlineKeyboardButton(text=i.answer))

    await bot.send_photo(message.chat.id, quest_message.image_path)
    await message.answer(quest_message.text)

    return


@dp.message_handler(commands='start')
async def init_command(message: types.Message):
    view_message(message, 'example')


if __name__ == '__main__':
    executor.start_polling(dp)
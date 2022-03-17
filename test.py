import asyncio
from auth_data import bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked
# import aiogram.utils.markdown as fmt


bot = Bot(bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await asyncio.sleep(2.0)
    await message.reply('Hello world!')


@dp.message_handler(commands=['button'])
async def buttom_text_message(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Yes', 'No']
    keyboard.add(*buttons)
    await message.answer('You Gay?', reply_markup=keyboard)


@dp.message_handler(commands=['author'])
async def author_message(message: types.Message):
    await message.answer('Вот:')
    buttons = [
        types.InlineKeyboardButton(text="Larinenok", url="https://github.com"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)


@dp.message_handler(lambda message: message.text == 'Yes')
async def yes_answer(message: types.Message):
    await message.reply('Ok', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == 'No')
async def yes_answer(message: types.Message):
    await message.reply('...', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler()
async def any_text_message(message: types.Message):
    # await asyncio.sleep(2.0)
    # print(message.text)
    await message.answer(
        f'Привет, {message.text}!\n',
        ''
    )


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


if __name__ == "__main__":
    executor.start_polling(dp)
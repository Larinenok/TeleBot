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
    buttons = [
        types.InlineKeyboardButton(text='Исходный код', url='https://github.com/Larinenok/TeleBot.git'),
        types.InlineKeyboardButton(text='Larinenok', url='https://t.me/+_pXEFqoYZdk2NTUy')
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    await message.answer('Вот:', reply_markup=keyboard)


@dp.message_handler(commands=['random'])
async def random_value(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text='Random?', callback_data='random_value'),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    await message.answer('randint(1, 10)', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Yes')
async def yes_answer(message: types.Message):
    await message.reply('Ok', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == 'No')
async def yes_answer(message: types.Message):
    await message.reply('...', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['photo'])
async def send_photo(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile('media/images/full_example.jpg'))


########################
# fabnum - префикс, action - название аргумента, которым будем передавать значение
callback_numbers = CallbackData("fabnum", "action")
user_data = {}


def get_keyboard_fab():
    buttons = [
        types.InlineKeyboardButton(text="-1", callback_data=callback_numbers.new(action="decr")),
        types.InlineKeyboardButton(text="+1", callback_data=callback_numbers.new(action="incr")),
        types.InlineKeyboardButton(text="Подтвердить", callback_data=callback_numbers.new(action="finish"))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(MessageNotModified):
        await message.edit_text(f"Укажите число: {new_value}", reply_markup=get_keyboard_fab())


@dp.message_handler(commands="numbers_fab")
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard_fab())


@dp.callback_query_handler(callback_numbers.filter(action=["incr", "decr"]))
async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(call.from_user.id, 0)
    action = callback_data["action"]
    if action == "incr":
        user_data[call.from_user.id] = user_value + 1
        await update_num_text_fab(call.message, user_value + 1)
    elif action == "decr":
        user_data[call.from_user.id] = user_value - 1
        await update_num_text_fab(call.message, user_value - 1)
    await call.answer()


@dp.callback_query_handler(callback_numbers.filter(action=["finish"]))
async def callbacks_num_finish_fab(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)
    await call.message.edit_text(f"Итого: {user_value}")
    await call.answer()
########################


@dp.message_handler()
async def any_text_message(message: types.Message):
    # await asyncio.sleep(2.0)
    # print(message.text)
    await message.answer(
        f'Привет, {message.text}!\n',
        # ''
    )


@dp.callback_query_handler(text='random_value')
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 10)))
    await call.answer()


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    print(f'Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}')
    return True


if __name__ == '__main__':
    executor.start_polling(dp)
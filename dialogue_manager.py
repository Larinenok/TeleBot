import asyncio
from auth_data import bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData
from json_reader import load_message_by_id


bot = Bot(bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
callback_numbers = CallbackData('fabnum', 'action')
quest = {}


async def view_message(message: types.Message, message_id: str):
    quest_message = load_message_by_id(message_id)
    varinats = ''
    buttons = []
    quest[message.from_user.id] = quest_message
    for i in quest_message.Answers:
        varinats += i.text + '\n'
        buttons.append(types.InlineKeyboardButton(text=i.answer, callback_data=callback_numbers.new(action=i.answer)))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    media = types.MediaGroup()
    media.attach_photo(types.InputFile(quest_message.image_path), quest_message.text)
    await bot.send_media_group(chat_id=message.chat.id, media=media)
    await asyncio.sleep(2.0)
    await message.answer(varinats, reply_markup=keyboard)


@dp.message_handler(commands='start')
async def init_command(message: types.Message):
    await view_message(message, 'example')       


@dp.callback_query_handler(callback_numbers.filter(action=['1', '2', '3', '4']))
async def move_to_message(call: types.CallbackQuery, callback_data: dict):
    action = callback_data['action']
    quest_value = quest.get(call.from_user.id)
    variants = ''
    for i in quest_value.Answers:
        if (i.answer == action):
            answer_id = i.id
            variants += '<b>' + i.text + '</b>' + '\n'
        else:
            variants += i.text + '\n'

    await call.message.edit_text(variants, reply_markup=None)
    await view_message(call.message, answer_id)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp)
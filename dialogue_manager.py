from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InputMediaPhoto, FSInputFile
import asyncio

# Инициализация бота
from auth_data import bot_token
from json_reader import load_message_by_id, get_quizes


# Создаем подкласс CallbackData
class QuizCallbackData(CallbackData, prefix='action'):
    action: str
    is_init: bool

bot = Bot(
    token=bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

quest = {}

async def choice_qiuz(message: Message):
    quizes = get_quizes()
    variants = ''
    buttons = []

    for i, name in enumerate(quizes):
        variants += name + '\n'
        buttons.append(
            types.InlineKeyboardButton(
                text=str(i + 1),
                callback_data=QuizCallbackData(action=name, is_init=True).pack()
            )
        )

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])

    await bot.send_message(message.chat.id, text='Выберете quiz:')
    await message.answer(variants, reply_markup=keyboard)

async def view_message(message: Message, message_id: str):
    quest_message = load_message_by_id(message_id)
    variants = ''
    buttons = []
    quest[message.chat.id] = quest_message

    for i in quest_message.Answers:
        variants += i.text + '\n'
        buttons.append(
            types.InlineKeyboardButton(
                text=i.answer,
                callback_data=QuizCallbackData(action=i.answer, is_init=False).pack()
            )
        )
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])
    
    # Корректное создание объекта InputMediaPhoto
    media = [InputMediaPhoto(media=FSInputFile(quest_message.image_path), caption=quest_message.text)]
    
    await bot.send_media_group(chat_id=message.chat.id, media=media)
    await asyncio.sleep(2.0)
    await message.answer(variants, reply_markup=keyboard)

async def stop_message(message: Message):
    await bot.send_message(message.chat.id, 'Вы прошли данную викторину!\nВот ваши результаты:\nПравильные ответы: 4 из 5')


@dp.message(Command(commands=['start']))
async def init_command(message: Message):
    await choice_qiuz(message)
    # await view_message(message, 'example')


@dp.callback_query(QuizCallbackData.filter())
async def move_to_message(call: CallbackQuery, callback_data: QuizCallbackData):
    action = callback_data.action
    quest_value = quest.get(call.from_user.id)
    variants = ''
    answer_id = None

    if quest_value and not callback_data.is_init:
        for i in quest_value.Answers:
            if i.answer == action:
                answer_id = i.id
                variants += f'<b>{i.text}</b>\n'
            else:
                variants += f'{i.text}\n'
    else:
        for name in get_quizes():
            if  name == action:
                answer_id = action
                variants += f'<b>{name}</b>\n'
            else:
                variants += f'{name}\n'

    await call.message.edit_text(variants)
    if answer_id == 'exit':
        await stop_message(call.message)
    else:
        await view_message(call.message, answer_id)
    await call.answer()


if __name__ == '__main__':
    dp.run_polling(bot)

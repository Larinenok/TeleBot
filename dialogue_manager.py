from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InputMediaPhoto, FSInputFile
import asyncio

# Инициализация бота
from auth_data import bot_token
from json_reader import load_message_by_id, get_quizes, load_quize_by_id
from db_utils import add_user, add_quiz_result, get_user_quiz_results


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
    quest[message.chat.id] = [quest_message, quest[message.chat.id][1]]

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

async def stop_message(message: Message, correct_answers, total_questions):
    await bot.send_message(message.chat.id, f'Вы прошли данную викторину!\nВот ваши результаты:\nПравильные ответы: {correct_answers} из {total_questions}')


@dp.callback_query(QuizCallbackData.filter())
async def move_to_message(call: CallbackQuery, callback_data: QuizCallbackData):
    action = callback_data.action
    quest_value = quest.get(call.from_user.id)
    variants = ''
    answer_id = None

    if quest_value and not callback_data.is_init:
        for i in quest_value[0].Answers:
            if i.answer == action:
                answer_id = i.id
                if i.is_true:
                    variants += f'<b>{i.text}</b> ✅\n'
                    quest_value[1] += 1
                else:
                    variants += f'<b>{i.text}</b> ❌\n'
            else:
                variants += f'{i.text}\n'
    else:
        for name in get_quizes():
            if  name == action:
                answer_id = load_quize_by_id(name).id
                variants += f'<b>{name}</b>\n'
            else:
                variants += f'{name}\n'

    await call.message.edit_text(variants)
    if answer_id == 'exit':
        add_quiz_result(
            quiz_name=quest_value[0].id,
            user_id=call.from_user.id,
            correct_answers=quest_value[1],
            total_questions=quest_value[0].total_questions,
        )

        await stop_message(call.message, quest_value[1], quest_value[0].total_questions)
    else:
        await view_message(call.message, answer_id)
    await call.answer()

@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.reply("Я могу помочь с определенными командами. Используйте /start, /stats и /info.")

@dp.message(Command("info"))
async def send_info(message: types.Message):
    await message.reply("Этот бот был создан для создания и прохождения викторин.")

@dp.message(Command("stats"))
async def send_stats(message: types.Message):
    results = get_user_quiz_results(user_id=message.from_user.id)
    if not results:
        await message.answer("Вы пока не участвовали в викторинах.")
        return

    response = "Ваши результаты викторин:\n\n"
    for result in results:
        date_obj = datetime.fromisoformat(result[3])
        date = date_obj.strftime('%d-%m-%Y %H:%M')
        response += (
            f"Викторина: {result[0]}\n"
            f"Правильные ответы: {result[1]}/{result[2]}\n"
            f"Дата: {date}\n\n"
        )
    await message.answer(response)

@dp.message(Command(commands=['start']))
async def init_command(message: Message):
    add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    quest[message.chat.id] = [None, 0]
    await choice_qiuz(message)

async def on_start():
    commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/help", description="Получить помощь"),
        BotCommand(command="/info", description="Информация о боте"),
        BotCommand(command="/stats", description="Информация о результатах викторин"),
    ]
    await bot.set_my_commands(commands)


if __name__ == '__main__':
    dp.startup.register(on_start)
    dp.run_polling(bot)

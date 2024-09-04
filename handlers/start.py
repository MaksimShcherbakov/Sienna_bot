import asyncio
import os.path
import re

from aiogram.utils.chat_action import ChatActionSender
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from keyboards.all_kb import main_kb, create_spec_kb, create_rat
from keyboards.inline_kbs import ease_link_kb, get_inline_kb, inline_kb_chat
from utils.utils import get_random_person
from keyboards.inline_kbs import create_qst_inline_kb
from create_bot import questions, bot, admins, all_media_dir
from filters.is_admin import IsAdmin
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

start_router = Router()
questionnaire_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Привет! Меня зовут Сиенна! Для ознакомления с доступными функциями можешь воспользовтаться командами из "Menu"',
        reply_markup=main_kb(message.from_user.id))


@start_router.message(Command('start_2'))
async def cmd_start_2(message: Message):
    await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()',
                         reply_markup=ease_link_kb())


@start_router.message(F.text == '/start_3')
async def cmd_start_3(message: Message):
    await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!',
                         reply_markup=create_rat())


@start_router.message(F.text == 'Давай инлайн!')
async def get_inline_btn_link(message: Message):
    await message.answer('Вот тебе!', reply_markup=get_inline_kb())


@start_router.callback_query(F.data == 'get_person')
async def send_random_person(call: CallbackQuery):
    await call.answer('Генерирую случайного пользователя', show_alert=False)
    user = get_random_person()
    formatted_message = (
        f"👤 <b>Имя:</b> {user['name']}\n"
        f"🏠 <b>Адрес:</b> {user['address']}\n"
        f"📧 <b>Email:</b> {user['email']}\n"
        f"📞 <b>Телефон:</b> {user['phone_number']}\n"
        f"🎂 <b>Дата рождения:</b> {user['birth_date']}\n"
        f"🏢 <b>Компания:</b> {user['company']}\n"
        f"💼 <b>Должность:</b> {user['job']}\n"
    )
    await call.message.answer(formatted_message)


@start_router.message(Command('faq'))
async def cmd_faq(message: Message):
    await message.answer('Сообщение с инлайн клавиатурой с вопросами', reply_markup=create_qst_inline_kb(questions))


@start_router.callback_query(F.data.startswith('qst_'))
async def cmd_start(call: CallbackQuery):
    await call.answer()
    qst_id = int(call.data.replace('qst_', ''))
    qst_data = questions[qst_id]
    msg_text = f'Ответ на вопрос {qst_data.get("qst")}\n\n' \
               f'<b>{qst_data.get("answer")}</b>\n\n' \
               f'Выбери другой вопрос:'
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await call.message.answer(msg_text, reply_markup=create_qst_inline_kb(questions))


@start_router.message(Command(commands=['settings', 'about']))
async def univers_cmd_handler(message: Message, command: CommandObject):
    command_args: str = command.args
    command_name = 'settings' if 'settings' in message.text else "about"
    response = f'Была вызвана команда /{command_name}'
    if command_args:
        response += f' с меткой <b>{command_args}</b>'
    else:
        response += ' без метки'
    await message.answer(response)


@start_router.message(F.text.lower().contains('подписывайся'), IsAdmin(admins))
async def process_find_word(message: Message):
    await message.answer('В твоем сообщении было найдено слово "подписывайся", а у нас такое писать запрещено!')


@start_router.message(F.text.lower().contains('подписывайся'))
async def process_find_word(message: Message):
    await message.answer('В твоем сообщении было найдено слово "подписывайся", а у нас такое писать запрещено!')


@start_router.message(F.text.regexp(r'(?i)^Здарова, .+'))
async def process_find_reg(message: Message):
    await message.answer('И тебе здарова! Че нада?')





@start_router.message(F.text.lower().contains('охотник'))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Я думаю, что ты тут про радугу рассказываешь')

    await bot.send_message(chat_id=message.from_user.id, text='Для меня это слишком просто')

    msg = await message.reply('Ну вот что за глупости!?')

    await bot.send_message(chat_id=message.from_user.id, text='Хотя, это забавно...',
                           reply_to_message_id=msg.message_id)

    await bot.forward_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id,
                              message_id=msg.message_id)

    data_task = {'user_id': message.from_user.id, 'full_name': message.from_user.full_name,
                 'username': message.from_user.username, 'message_id': message.message_id, 'date': message.date}
    print(data_task)


@start_router.message(Command('test_edit_msg'))
async def cmd_start(message: Message, state: FSMContext):
    msg = await message.answer('Привет!')
    await asyncio.sleep(2)
    old_text = msg.text
    await msg.delete()
    await message.answer(old_text, reply_markup=main_kb(message.from_user.id))


@start_router.message(F.text.contains('🇺🇸'))
async def cmd_start(message: Message, state: FSMContext):
    audio_file = FSInputFile(path=os.path.join(all_media_dir, 'why_usa_flag.mp3'), filename='У меня вопрос...')
    await message.answer_audio(audio=audio_file)


class Form(StatesGroup):
    name = State()
    age = State()


def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group())
    else:
        return None


@questionnaire_router.message(Command('start_questionnaire'))
async def start_questionnaire_process(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Привет. Напиши как тебя зовут: ')
    await state.set_state(Form.name)


@questionnaire_router.message(F.text, Form.name)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Супер! А теперь напиши сколько тебе полных лет: ')
    await state.set_state(Form.age)


@questionnaire_router.message(F.text, Form.age)
async def capture_age(message: Message, state: FSMContext):
    check_age = extract_number(message.text)

    if not check_age or not (1 <= check_age <= 100):
        await message.reply('Пожалуйста, введите корректный возраст (число от 1 до 100).')
        return
    await state.update_data(age=check_age)

    data = await state.get_data()
    msg_text = (f'Вас зовут <b>{data.get("name")}</b> и вам <b>{data.get("age")}</b> лет. '
                f'Спасибо за то что ответили на мои вопросы.')
    await message.answer(msg_text)
    await state.clear()

# @start_router.message(F.text == 'Настройка бота')
# async def cmd_bot_settings(message: Message):
#     await message.answer('Давайте настроим бота',
#                          reply_markup=inline_kb_chat())

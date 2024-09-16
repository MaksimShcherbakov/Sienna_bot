import asyncio
import os.path
import re

import keyboards.all_kb as all_kbs
import keyboards.inline_kbs as inline_kbs
import create_bot as create_bot
import filters.is_admin as admin
import database.requests as req

from aiogram.utils.chat_action import ChatActionSender
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.utils import get_random_person, extract_number

start_router = Router()
questionnaire_router = Router()


class Form(StatesGroup):
    gender = State()
    age = State()
    full_name = State()
    user_login = State()
    photo = State()
    about = State()
    refer_id = State()
    check_state = State()


@start_router.message(Command('registration'))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=create_bot.bot, chat_id=message.chat.id):
        user_info = await req.get_user_data(user_id=message.from_user.id)

    if user_info:
        await message.answer('Привет. Я вижу, что ты зарегистрирован, а значит тебе можно '
                             'посмотреть, как выглядит твой профиль.',
                             reply_markup=all_kbs.main_kb(message.from_user.id))
    else:
        await message.answer('Привет. Для начала выбери свой пол:', reply_markup=all_kbs.gender_kb())
        await state.set_state(Form.gender)


@start_router.message(Command('start_3'))
async def cmd_start_2(message: Message):
    await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()',
                         reply_markup=inline_kbs.ease_link_kb())


@start_router.message(F.text == '/start_4')
async def cmd_start_3(message: Message):
    await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!',
                         reply_markup=all_kbs.create_rat())


@start_router.message(F.text == 'Давай инлайн!')
async def get_inline_btn_link(message: Message):
    await message.answer('Вот тебе!', reply_markup=inline_kbs.get_inline_kb())


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
    await message.answer('Сообщение с инлайн клавиатурой с вопросами',
                         reply_markup=inline_kbs.create_qst_inline_kb(create_bot.questions))


@start_router.callback_query(F.data.startswith('qst_'))
async def cmd_start(call: CallbackQuery):
    await call.answer()
    qst_id = int(call.data.replace('qst_', ''))
    qst_data = create_bot.questions[qst_id]
    msg_text = f'Ответ на вопрос {qst_data.get("qst")}\n\n' \
               f'<b>{qst_data.get("answer")}</b>\n\n' \
               f'Выбери другой вопрос:'
    async with ChatActionSender(bot=create_bot.bot, chat_id=call.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await call.message.answer(msg_text, reply_markup=inline_kbs.create_qst_inline_kb(create_bot.questions))


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


@start_router.message(F.text.lower().contains('украин'), admin.IsAdmin(create_bot.admins))
async def process_find_word(message: Message):
    await message.answer('В твоем сообщении было найдено упоминание Украины, а у нас такое писать запрещено!')


@start_router.message(F.text.lower().contains('украин'))
async def process_find_word(message: Message):
    await message.answer('В твоем сообщении было найдено упоминание Украины, а у нас такое писать запрещено!')


@start_router.message(F.text.regexp(r'(?i)^Здарова, .+'))
async def process_find_reg(message: Message):
    await message.answer('И тебе здарова! Че нада?')


@start_router.message(F.text.lower().contains('охотник'))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Я думаю, что ты тут про радугу рассказываешь')

    await create_bot.bot.send_message(chat_id=message.from_user.id, text='Для меня это слишком просто')

    msg = await message.reply('Ну вот что за глупости!?')

    await create_bot.bot.send_message(chat_id=message.from_user.id, text='Хотя, это забавно...',
                                      reply_to_message_id=msg.message_id)

    await create_bot.bot.forward_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id,
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
    await message.answer(old_text, reply_markup=all_kbs.main_kb(message.from_user.id))


@start_router.message(F.text.contains('🇺🇸'))
async def cmd_start(message: Message, state: FSMContext):
    audio_file = FSInputFile(path=os.path.join(create_bot.all_media_dir, 'why_usa_flag.mp3'),
                             filename='У меня вопрос...')
    await message.answer_audio(audio=audio_file)


@questionnaire_router.message(Command('start_questionnaire'))
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=create_bot.bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Привет. Для начала выбери свой пол: ', reply_markup=all_kbs.gender_kb())
    await state.set_state(Form.gender)


@questionnaire_router.message((F.text.lower().contains('мужчина')) | (F.text.lower().contains('женщина')), Form.gender)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(gender=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=create_bot.bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer("Супер! А теперь напиши сколько тебе полных лет:", reply_markup=ReplyKeyboardRemove())
    await state.set_state((Form.age))


@questionnaire_router.message(F.text, Form.gender)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    async with ChatActionSender.typing(bot=create_bot.bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Пожалуйста, выбери вариант из тех что в клавиатуре: ', reply_markup=all_kbs.gender_kb())
    await state.set_state(Form.gender)


@questionnaire_router.message(F.text, Form.age)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if not (re.fullmatch(r'\d+', message.text.strip())):
        await message.reply('Введите полный возраст в текстовом сообщении без специальных символов')
        return
    check_age = extract_number(message.text)
    if not check_age or not (1 <= int(message.text) <= 100):
        await message.reply('Пожалуйста, введите корректный возраст (число от 1 до 100)')
        return

    await state.update_data(age=check_age)
    await message.answer('Теперь укажите свое полное имя:')
    await state.set_state(Form.full_name)


@questionnaire_router.message(F.text, Form.full_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    text = 'Теперь укажите Ваш логин, который будет использоваться в боте'

    if message.from_user.username:
        text += ' или нажмите на кнопку ниже и в этом случае Вашим логином будет логин ТГ'
        await message.answer(text, reply_markup=inline_kbs.get_login_tg())
    else:
        text += ' : '
        await message.answer(text)

    await state.set_state(Form.user_login)


@questionnaire_router.callback_query(F.data, Form.user_login)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Беру логин телеграмм профиля')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(user_login=call.from_user.username)
    await call.message.answer('А теперь отправьте фото, которое будет использоваться в вашем профиле: ')
    await state.set_state(Form.photo)


@questionnaire_router.message(F.text, Form.user_login)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(user_login=message.from_user.username)
    await message.answer('А теперь отправьте фото, которое будет использоваться в вашем профиле: ')
    await state.set_state(Form.photo)


@questionnaire_router.message(F.photo, Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer('А теперь расскажите пару слов о себе: ')
    await state.set_state(Form.about)


@questionnaire_router.message(F.document.mime_type.startswith('image/'), Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    photo_id = message.document.file_id
    await state.update_data(photo=photo_id)
    await message.answer('А теперь расскажите пару слов о себе:')
    await state.set_state(Form.about)


@questionnaire_router.message(F.document, Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте фото!')
    await state.set_state(Form.photo)


@questionnaire_router.message(F.text, Form.about)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer(
        'Если у вас есть реферальный код, пожалуйста, напишите ниже. Если нет, нажмите "Пропустить"',
        reply_markup=all_kbs.skip_kb('Введите код:'))
    await state.set_state(Form.refer_id)


@questionnaire_router.message(F.text, Form.refer_id)
async def referer_check(message: Message, state: FSMContext):
    referral_code = message.text
    if not (re.fullmatch(r'\d+', referral_code.strip())):
        await message.reply('Код должен состоять только из цифр')
        return
    if int(referral_code) == message.from_user.id:
        await message.reply('Хорошая попытка, но не засчитано}')
        return
    if not await req.check_code_exist(int(referral_code)):
        await message.reply('Ваш код недействительный. Введите корректный код или нажмите "Пропустить".')
        return
    await state.update_data(refer_id=int(referral_code))
    await proceed_to_check(message, state)


async def proceed_to_check(message: Message, state: FSMContext):
    data = await state.get_data()
    caption = (
        f'Пожалуйста, проверьте все ли верно: \n\n'
        f'<b>Полное имя</b>: {data.get("full_name")}\n'
        f'<b>Пол</b>: {data.get("gender")}\n'
        f'<b>Возраст</b>: {data.get("age")} лет\n'
        f'<b>Логин в боте</b>: {data.get("user_login")}\n'
        f'<b>О себе</b>: {data.get("about")}'
    )

    await message.answer_photo(photo=data.get('photo'), caption=caption, reply_markup=inline_kbs.check_data())
    await state.set_state(Form.check_state)


@questionnaire_router.callback_query(F.data == 'correct', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Данные сохранены')
    user_data = await state.get_data()
    await req.add_user(user_data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Благодарю за регистрацию. Ваши данные успешно сохранены!')
    await state.clear()


@questionnaire_router.callback_query(F.data == 'incorrect', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Запускаем сценарий с начала')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Привет. Для начала выбери свой пол: ', reply_markup=all_kbs.gender_kb())
    await state.set_state(Form.gender)


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать!', reply_markup=all_kbs.main)


@start_router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите вариант из каталога', reply_markup=await inline_kbs.categories())


@start_router.callback_query(F.data.startswith('category_'))
async def category_selected(call: CallbackQuery):
    category_id = int(call.data.split('_')[1])
    await call.message.answer(f'Товары по выбранной категории:', reply_markup=await inline_kbs.products(category_id))
    await call.answer("")


@start_router.callback_query(F.data.startswith('product_'))
async def product_selected(call: CallbackQuery):
    product_id = int(call.data.split('_')[1])
    product = await req.get_product(product_id=product_id)
    await call.message.answer(f'<b>{product.name}</b>\n\n{product.description}\n\n{product.price}$')
    await call.answer(f"Вы выбрали {product.name}")


@start_router.message(F.text.contains('Профиль'))
async def start_profile(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=create_bot.bot, chat_id=message.chat.id):
        user_info = await req.get_user_data(message.from_user.id)
        profile_message = (
            f"<b>👤 Профиль пользователя:</b>\n"
            f"<b>💼 Логин:</b> @{user_info.user_login}\n"
            f"<b>📛 Полное имя:</b> {user_info.full_name}\n"
            f"<b>🧑‍🦰 Пол:</b> {user_info.gender}\n"
            f"<b>🎂 Возраст:</b> {user_info.age}\n"
            f"<b>📅 Дата регистрации:</b> {user_info.date_reg}\n"
            f"<b>📝 О себе:</b> {user_info.about}\n"
        )
        await message.answer_photo(photo=user_info.photo, caption=profile_message)

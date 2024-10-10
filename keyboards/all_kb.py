from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType, BotCommand, \
    BotCommandScopeDefault, InlineKeyboardButton
from create_bot import admins
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from database.requests import get_categories


def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="👤 Профиль")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard


def create_spec_kb():
    kb_list = [
        [KeyboardButton(text="Отправить гео", request_location=True)],
        [KeyboardButton(text="Поделиться номером", request_contact=True)],
        [KeyboardButton(text="Отправить викторину/опрос", request_poll=KeyboardButtonPollType())]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list,
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder="Воспользуйтесь специальной клавиатурой:")
    return keyboard


def create_rat():
    builder = ReplyKeyboardBuilder()
    for item in [str(i) for i in range(1, 11)]:
        builder.button(text=item)
    builder.button(text='Назад')
    builder.adjust(4, 4, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def gender_kb():
    kb_list = [
        [KeyboardButton(text='👨‍🦱 Мужчина')], [KeyboardButton(text='👩‍🦱 Женщина')]
    ]
    keyboards = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True,
                                    input_field_placeholder="Выберите пол:")
    return keyboards


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Контакты')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт ниже')


def skip_kb(info):
    kb_list = [[KeyboardButton(text='Пропустить')]]
    keyboards = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True,
                                    input_field_placeholder=info)
    return keyboards


def start_kb():
    kb_list = [[KeyboardButton(text="▶️ Начать диалог")]]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Чтоб начать диалог с ботом жмите 👇:"
    )


def stop_speak():
    kb_list = [[KeyboardButton(text="❌ Завершить диалог")]]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Чтоб завершить диалог с ботом жмите 👇:"
    )

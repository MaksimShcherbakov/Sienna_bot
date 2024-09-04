from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Мой VK", url='https://vk.com/id25635630')],
        [InlineKeyboardButton(text="Мой Telegram", url='https://t.me/pro100_shcherbakov')],
        [InlineKeyboardButton(text="Веб приложение", web_app=WebAppInfo(url="https://tg-promo-bot.ru/questions"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def get_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Генерировать пользователя", callback_data='get_person')],
        [InlineKeyboardButton(text="На главную", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def inline_kb_chat():
    inline_kb_chat = [
        [InlineKeyboardButton(text="Создать ассистента", callback_data='make_assistance')],
        [InlineKeyboardButton(text="На главную", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_chat)

def create_qst_inline_kb(questions: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for question_id, question_data in questions.items():
        builder.row(
            InlineKeyboardButton(
                text=question_data.get('qst'),
                callback_data=f'qst_{question_id}'
            )
        )
    builder.row(
        InlineKeyboardButton(
            text='На главную',
            callback_data='back_home'
        )
    )
    builder.adjust(1)
    return builder.as_markup()

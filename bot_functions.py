# from aiogram.types import Message
# from constants import CALL_NAMES
# from aiogram import Dispatcher
#
# dp = Dispatcher()
# @dp.message()
# async def check_call(message: Message) -> bool:
#     words = message.text.split()
#     first_word = words[0].lower()
#     if first_word in CALL_NAMES or first_word[:-1] in CALL_NAMES:
#         if len(words) > 1:
#             # word_to_delete = first_word + ', ' if first_word + ',' in CALL_NAMES else first_word + ' '
#             # message_text = message.text[len(word_to_delete):]
#             try:
#                 # await message.bot.send_message(chat_id=message.chat.id, text=message_text)
#                 return True
#             except TypeError:
#                 await message.answer("Nice try!")
#                 return False
#
#         else:
#             await message.bot.send_message(chat_id=message.chat.id, text='Чем я могу помочь?')
#             return False
#
#
# @dp.message()
# async def get_text_from_message(message: Message):
#     if check_call(message):
#         words = message.text.split()
#         first_word = words[0].lower()
#         word_to_delete = first_word + ', ' if first_word + ',' in CALL_NAMES else first_word + ' '
#         message_text = message.text[len(word_to_delete):]
#         await message.bot.send_message(chat_id=message.chat.id, text=message_text)
#     return

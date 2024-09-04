# import asyncio
# import logging
# import sys
# import requests
#
#
# from aiogram import Bot, html
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from constants import TOKEN_SIENNA_BOT, OPENAI_API_KEY, CALL_NAMES
# from bot_functions import get_text_from_message, dp
#
#
# async def main() -> None:
#     bot = Bot(token=TOKEN_SIENNA_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     await dp.start_polling(bot)
#
#
#
#
# assistance_headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {OPENAI_API_KEY}",
#     "OpenAI-Beta": "assistants=v2"
# }
#
# # create_assistance_data = {
# #     "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
# #     "name": "Math Tutor",
# #     "tools": [{"type": "code_interpreter"}],
# #     "model": "gpt-4o-mini"
# # }
#
#
# response = requests.get("https://api.openai.com/v1/assistants?order=desc&limit=20", headers=assistance_headers)
#
# print(response.json())
#
#
# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
#
# @dp.message()
# async def handle_message(message: Message) -> None:
#     response_second = get_text_from_message(message.text)
#     await message.answer(response_second)
#
# # @dp.message()
# # async def echo_handler(message: Message) -> None:
# #     words = message.text.split()
# #     first_word = words[0].lower()
# #     if (first_word in CALL_NAMES or first_word[:-1] in CALL_NAMES):
# #         if len(words) > 1:
# #             word_to_delete = first_word + ', ' if first_word + ',' in CALL_NAMES else first_word + ' '
# #             message_text = message.text[len(word_to_delete):]
# #
# #             try:
# #                 await message.bot.send_message(chat_id=message.chat.id, text=message_text)
# #             except TypeError:
# #                 await message.answer("Nice try!")
# #
# #         else:
# #             await message.bot.send_message(chat_id=message.chat.id, text='Чем я могу помочь?')
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())

# from openai import OpenAI
#
# dialog_history = []
#
# while True:
#     user_input = input('Введите ваше сообщение ("stop" для завершения): ')
#
#     if user_input.lower() == 'stop':
#         break
#
#     dialog_history.append({
#         'role': 'user',
#         'content': user_input,
#     })
#
#     response = client.chat.completions.create(
#         model='llama3:8b',
#         messages=dialog_history,
#     )
#
#     response_content = response.choices[0].message.content
#     print('Ответ модели: ', response_content)
#
#     dialog_history.append({
#         'role': 'assistant',
#         'content': response_content,
#     })

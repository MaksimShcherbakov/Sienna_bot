from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

chat_router = Router()

class CreateAssistance(StatesGroup):
    waiting_for_name = State()
    waiting_for_instruction = State()



@chat_router.callback_query(F.data == 'make_assistance')
async def create_assistance(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите имя нового ассистента:')
    await CreateAssistance.waiting_for_name.set()

@chat_router.message(state=CreateAssistance.waiting_for_name)
async def get_assistance_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Теперь введите инструкция для ассиситента:')
    await CreateAssistance.waiting_for_instruction.set()

@chat_router.message(state=CreateAssistance.waiting_for_instruction)
async def get_assistance_instruction(message: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['name']
    instruction = message.text

    result = await create_assistance(name, instruction)

    await message.answer(f"Ассистент создан: {result}")
    await state.finish()
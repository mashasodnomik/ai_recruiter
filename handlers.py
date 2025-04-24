import os
import google.generativeai as genai
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext



genai.configure(api_key="AIzaSyBeXA5UN__Wzt9QcmjB2KEMrIspFc33tXQ")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="Ты помощник HR-менеджера и ты помогаешь оптимизировать задачу рекрутинга. Ты должен сравнивать резюме и давать оценку, кого взять на работу, а кого нет.",
)

chat_session = model.start_chat(history=[])

import app.keyboards as kb

router = Router()

class CompareCandidates(StatesGroup):
    criteria = State()  # Запоминаем введенные пользователем параметры

@router.callback_query(F.data == "compare")
async def compare_candidates(callback: CallbackQuery, state: FSMContext):
    """Хэндлер для кнопки 'Сравнить кандидатов'"""
    await state.set_state(CompareCandidates.criteria)
    await callback.message.answer("Введите параметры для сравнения кандидатов (например: 'Опыт работы, навыки, образование').")


@router.message(CompareCandidates.criteria)
async def process_criteria(message: Message, state: FSMContext):
    """Получаем критерии сравнения от пользователя, отправляем в Gemini и выдаем ответ"""
    user_input = message.text
    await state.clear()  # Очищаем состояние

    # Отправляем сообщение в Gemini
    response = chat_session.send_message(f"Сравни кандидатов по следующим параметрам: {user_input}")

    # Отправляем ответ пользователю
    await message.answer(f"Вот результат сравнения кандидатов:\n\n{response.text}")


class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Здравствуйте, это рекрутинг бот! выберете кто Вы', reply_markup=kb.role)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи')


@router.message(F.text == 'Эйчар менеджер')
async def catalog(message: Message):
    await message.answer('Что Вы хотите сделать?', reply_markup=kb.hr)

# @router.callback_query(F.data == 'compare')
# async def t_shirt(callback: CallbackQuery):
#     await callback.message.answer('Вы выбрали категорию футболок.')

# @router.callback_query(F.data == 'list_candid')
# async def t_shirt(callback: CallbackQuery):
#     await callback.answer('Вы выбрали категорию', show_alert=True)
#     await callback.message.answer('Вы выбрали категорию футболок.')

@router.message(F.text == 'Кандидат')
async def catalog(message: Message):
    await message.answer('Что Вы хотите сделать?', reply_markup=kb.applicant)

@router.callback_query(F.data == 't-shirt')
async def t_shirt(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию', show_alert=True)
    await callback.message.answer('Вы выбрали категорию футболок.')



@router.callback_query(F.data == 'status')
async def t_shirt(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию', show_alert=True)
    await callback.message.answer('Вы выбрали категорию футболок.')



@router.callback_query(F.data == 'apply')
async def apply(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.name)
    await callback.message.answer('Введите ваше имя')

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')


@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)
    await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)


@router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nНомер: {data["number"]}')
    await state.clear()
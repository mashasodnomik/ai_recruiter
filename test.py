import os
import google.generativeai as genai
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb  # Импорт клавиатур

# Настройка Gemini API
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

router = Router()


class CompareCandidates(StatesGroup):
    criteria = State()  # Запоминаем введенные пользователем параметры


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Здравствуйте, это рекрутинговый бот! Выберите, кто Вы", reply_markup=kb.role)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Вы нажали на кнопку помощи")


@router.message(F.text == "Эйчар менеджер")
async def hr_manager(message: Message):
    await message.answer("Что Вы хотите сделать?", reply_markup=kb.hr)


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
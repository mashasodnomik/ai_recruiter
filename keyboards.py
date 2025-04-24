from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                     [KeyboardButton(text='Корзина')],
                                     [KeyboardButton(text='Контакты'),
                                      KeyboardButton(text='О нас')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

role = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Эйчар менеджер'), KeyboardButton(text='Кандидат')]])

hr = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть список кандидатов', callback_data='list_candid')],
    [InlineKeyboardButton(text='Сравнить кандидатов', callback_data='compare')],
  ])

applicant = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подать резюме', callback_data='apply')],
    [InlineKeyboardButton(text='Посмотреть статус своего резюме', callback_data='status')],
  ])


get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True)]],
                                 resize_keyboard=True)

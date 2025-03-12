from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=
                           [[KeyboardButton(text='Вывод определенного банка')],
                           [KeyboardButton(text='Вывод всех банков')]],
                            resize_keyboard=True, 
                            input_field_placeholder='Выберите банк...')


ask_bank = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='Альфа Банк', callback_data='alpha_bank'),
                                InlineKeyboardButton(text='Беларусбанк', callback_data='belarusbank')],
                                [InlineKeyboardButton(text='Белагропромбанк', callback_data='belaroproprombank'),
                                InlineKeyboardButton(text='Белгазпромбанк', callback_data='belgazprombank')],
                                [InlineKeyboardButton(text='Приорбанк', callback_data='priorbank'),
                                InlineKeyboardButton(text='На главную', callback_data='_to_main'),]])
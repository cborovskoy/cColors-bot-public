from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_kb_for_main_menu(game_over: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if not game_over:
        builder.row(InlineKeyboardButton(text='1 вариант', callback_data='option_1'),
                    InlineKeyboardButton(text='2 вариант', callback_data='option_2'))
    else:
        builder.row(InlineKeyboardButton(text='Сыграть ещё', callback_data='new'))

    return builder.as_markup()

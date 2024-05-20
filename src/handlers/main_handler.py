from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile, CallbackQuery, InputMediaPhoto

from src.models.colors import Colors
from src.utils.keyboards import get_kb_for_main_menu
from src.utils.pic import make_pic, game_over_pic

router = Router()


async def send_playing_field(chat_id: int, bot: Bot, state: FSMContext, bot_msg_to_edit: Message = None):
    state_data = await state.get_data()
    game_over: bool = state_data.get('game_over', False)
    lvl: int = state_data.get('lvl', 1)
    new_colors: bool = state_data.get('new_colors', False)
    await state.update_data(game_over=game_over, lvl=lvl)

    if game_over:
        colors: Colors = state_data.get('colors')
        pic = game_over_pic(lvl=lvl, colors=colors)
    else:
        temp_colors = None if new_colors else state_data.get('colors')
        pic, colors = make_pic(lvl=lvl, colors=temp_colors)

    input_file = BufferedInputFile(file=pic.getvalue(), filename='img.png')
    kb = get_kb_for_main_menu(game_over=game_over)

    if bot_msg_to_edit:
        caption = f'{colors.main}' if game_over else None
        await bot_msg_to_edit.edit_media(media=InputMediaPhoto(media=input_file, caption=caption), reply_markup=kb)
    else:
        msg = await bot.send_photo(chat_id=chat_id, photo=input_file, reply_markup=kb)
        await state.update_data(playing_field_msg_id=msg.message_id)

    await state.update_data(new_colors=False, colors=colors)


@router.message()
async def user_msg_handler(message: Message, state: FSMContext):
    await message.delete()
    chat_id = message.from_user.id
    bot = message.bot

    state_data = await state.get_data()
    playing_field_msg_id: int = state_data.pop('playing_field_msg_id', None)
    game_over: bool = state_data.get('game_over', False)
    if playing_field_msg_id:
        if game_over:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=playing_field_msg_id, reply_markup=None)
        else:
            await bot.delete_message(chat_id=chat_id, message_id=playing_field_msg_id)
    await state.set_data(data=state_data)

    if game_over:
        await state.update_data(game_over=False, lvl=1, new_colors=True)

    await send_playing_field(chat_id=chat_id, bot=bot, state=state)


@router.callback_query()
async def main_menu_btn_handler(callback: CallbackQuery, state: FSMContext):
    bot = callback.bot
    chat_id = callback.from_user.id
    bot_msg = callback.message

    state_data = await state.get_data()
    lvl: int = state_data.get('lvl')
    colors: Colors = state_data.get('colors')

    if callback.data in ['option_1', 'option_2'] and colors:
        result = (colors.option_1 if callback.data == 'option_1' else colors.option_2) == colors.main
        new_lvl = lvl + (1 if result else 0)
        await state.update_data(game_over=not result, new_colors=True, lvl=new_lvl)
        await send_playing_field(chat_id=chat_id, bot=bot, state=state, bot_msg_to_edit=bot_msg)

    elif callback.data == 'new':
        await bot_msg.delete_reply_markup()
        await state.update_data(game_over=False, lvl=1, new_colors=True)
        await send_playing_field(chat_id=chat_id, bot=bot, state=state)

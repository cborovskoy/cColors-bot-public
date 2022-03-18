from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InputMediaPhoto

from main import make_pic

from settings import get_tg_token


def get_keyboard(game_over=False):
    if not game_over:
        inline_keyboard = [
            [
                InlineKeyboardButton(text='1 вариант', callback_data='var_1'),
                InlineKeyboardButton(text='2 вариант', callback_data='var_2'),

            ],
        ]
    else:
        inline_keyboard = [
            [
                InlineKeyboardButton(text='Сыграть ещё', callback_data='new'),
            ],
        ]
    return InlineKeyboardMarkup(inline_keyboard)


def message_handler(update: Update, context: CallbackContext):
    check_lvl(update, context)
    send_pic(update=update, context=context)


def callback_handler(update: Update, context: CallbackContext):
    check_lvl(update, context)
    callback_data = update.callback_query.data

    if callback_data == 'new':
        send_pic(update=update, context=context)

    elif callback_data.startswith('var_'):
        game_settings = context.chat_data['game_settings']
        v_color = game_settings[f'v{callback_data[-1]}_color']
        main_color = game_settings['main_color']

        if v_color == main_color:
            game_settings['lvl'] += 1
            send_pic(update=update, context=context, only_update_image=True)
        else:
            game_over(update, context, only_update_image=True)


def game_over(update: Update, context: CallbackContext, only_update_image=False):
    user_id = update.effective_user.id
    photo_path = f'pic_game_over_{user_id}.png'
    game_settings = context.chat_data['game_settings']
    msg_txt = f"{game_settings['main_color']}"

    if only_update_image:
        new_pic = InputMediaPhoto(media=open(photo_path, 'rb'),
                                  caption=msg_txt)
        context.bot.edit_message_media(chat_id=user_id,
                                       message_id=context.chat_data['msg_id'],
                                       media=new_pic,
                                       reply_markup=get_keyboard(game_over=True))

    game_settings['lvl'] = 1


def send_pic(update: Update, context: CallbackContext, only_update_image=False):
    user_id = update.effective_user.id

    try:
        context.bot.edit_message_reply_markup(chat_id=user_id,
                                              message_id=context.chat_data['msg_id'],
                                              reply_markup=None)
    except:
        pass

    game_settings = context.chat_data['game_settings']

    colors = make_pic(user_id=user_id, lvl=game_settings['lvl']-1)
    game_settings['main_color'] = colors['main']
    game_settings['v1_color'] = colors['var_1']
    game_settings['v2_color'] = colors['var_2']

    photo_path = f'pic_{user_id}.png'

    msg_txt = f"{'✅'*(game_settings['lvl']-1)}\n" \
              f"{game_settings['main_color']}"

    if only_update_image:
        new_pic = InputMediaPhoto(media=open(photo_path, 'rb'),
                                  caption=msg_txt)
        context.bot.edit_message_media(chat_id=user_id,
                                       message_id=context.chat_data['msg_id'],
                                       media=new_pic,
                                       reply_markup=get_keyboard())

    else:
        msg = context.bot.send_photo(chat_id=user_id,
                                     caption=msg_txt,
                                     photo=open(photo_path, 'rb'),
                                     reply_markup=get_keyboard())
        context.chat_data['msg_id'] = msg.message_id


def check_lvl(update: Update, context: CallbackContext):
    try:
        print(context.chat_data['game_settings'])
    except:
        context.chat_data['game_settings'] = {'lvl': 1}


def main():
    updater = Updater(
        token=get_tg_token(), use_context=True
    )

    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import queries
import say

CHOOSE_PACK, CHOOSE_MODE, CHOOSE_LANG, START_EX, CARD = (0, 1, 2, 3, 4)

selected_packs = {}
selected_cards = {}
learning_command = {}

modes = ["/Review", "/Learn"]


def begin(bot, update):
    packs = queries.active_packs(update.message.from_user.id)
    pack_list = []
    for i in packs:
        pack_list.append(i[1])
    # СДЕЛАТЬ enumerate
    msg = say.choose_a_pack + '\n' + '\n'.join(pack_list) + '\n' + say.begin_options
    update.message.reply_text(msg)
    return CHOOSE_PACK


def choose_pack(bot, update):
    n = update.message.text
    user_id = update.message.from_user.id
    selected_packs[user_id] = queries.active_packs(user_id)[n]

    reply_keyboard = [modes]
    update.message.reply_text(say.choose_mode,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOOSE_MODE


def start_review(bot, update):
    pass


def start_learn(bot, update):
    update.message.reply_text(say.start_mode_learning)
    user_id = update.message.from_user.id
    selected_cards[user_id] = queries.select_cards(user_id, selected_packs[user_id])
    make_list(selected_cards[user_id])
    update.message.reply_text(make_list + say.learning_mode_legend)

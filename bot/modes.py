from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import queries
import say
# import review

CHOOSE_PACK, CHOOSE_MODE, CHOOSE_REVIEW_TYPE, START_REVIEW, START_LEARN, REVIEW, LEARN, CHANGE_LANGUAGE = tuple(range(8))

selected_packs = {}
selected_cards = {} # можно ли смотреть из внешних файлов
learning_command = {}
language = {}

modes = ["Review", "Learn"]


def begin(bot, update):
    packs = queries.active_packs(update.message.from_user.id)
    pack_list = []
    for i in packs:
        pack_list.append(i[1])
    # СДЕЛАТЬ enumerate
    msg = say.choose_a_pack + '\n' + '\n'.join(pack_list) + '\n' + say.begin_options
    update.message.reply_text(msg)
    return CHOOSE_PACK


def change_language(bot, update):
    pass


def choose_pack(bot, update):
    n = update.message.text
    user_id = update.message.from_user.id
    selected_packs[user_id] = queries.active_packs(user_id)[n]

    reply_keyboard = [modes]
    update.message.reply_text(say.choose_mode,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOOSE_MODE


def choose_mode(bot, update):
    mode = update.message.text
    if mode == "Review":
        return CHOOSE_REVIEW_TYPE
    elif mode == "Learn":
        return START_LEARN


def choose_review_type(bot, update):
    return START_REVIEW


def start_learn(bot, update):
    pass


def start_review(bot, update):
    # просит выбрать язык
    return REVIEW


def review(bot, update):
    # принимает команды и достает карточку
    pass


def learn_end():
    pass


def end(bot, update):
    pass


def show_cards(user_id, lang=0, answer=None):
    # answer 0 is all answers
    res = ""
    for i in enumerate(list):
        res = res + str(i[0]) + ". " + i[1] + "\n"
    return res

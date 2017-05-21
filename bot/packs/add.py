from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, TelegramError
import say
from utils import user, row_markup, send
from db import queries
from db.enums import *
from menu import head_menu

END = ConversationHandler.END
START = 0
CHOOSE_PACK = 1


# TODO: Add pages support
def start(bot, update):
    return choose_pack(bot, update)


def choose_pack(bot, update):
    packs = map(lambda x: str(x[0]) + ': ' + x[1], queries.available_packs(user(update)))
    update.message.reply_text(say.choose_a_pack, reply_markup=row_markup(packs))
    return CHOOSE_PACK


def choose_pack_h(bot, update):
    colon_ind = update.message.text.find(':')
    try:
        pack_id = int(update.message.text[:colon_ind])
    except ValueError:
        update.message.reply_text('Invalid')
        return CHOOSE_PACK
    if queries.if_added(user(update), pack_id):
        send(update, say.already_added)
        return CHOOSE_PACK
    queries.add_pack(user(update), pack_id)
    return end(bot, update)


def end(bot, update):
    send(update, say.pack_added)
    head_menu(bot, update)
    return END

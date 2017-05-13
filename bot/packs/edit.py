from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import say
from utils import user
from db import queries

END = ConversationHandler.END
START = 0
CHOOSE_PACK = 1


_states = {}


def start(bot, update):
    _states[user(update)] = {}
    packs = map(lambda x: str(x[0]) + ': ' + x[1], queries.active_packs(user(update)))
    update.message.reply_text(say.choose_pack, reply_markup=ReplyKeyboardMarkup([[x] for x in packs], one_time_keyboard=True))
    return CHOOSE_PACK


def choose_pack(bot, update):
    state = _states[user(update)]
    colon_ind = update.message.text.find(':')
    try:
        pack_id = int(update.message.text[:colon_ind])
    except ValueError:
        update.message.reply_text('Invalid')
        return CHOOSE_PACK
    update.message.reply_text(str(queries.get_pack(pack_id)))
    return END

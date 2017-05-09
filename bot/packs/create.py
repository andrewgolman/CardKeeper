from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
import say
from utils import user
from db import queries

END = ConversationHandler.END
START = 0
CHOOSE_NAME = 1
CHOOSE_PRIVACY = 2

_states = {}


def start(bot, update):
    _states[user(update)] = {}
    update.message.reply_text(say.choose_pack_name)
    return CHOOSE_NAME


def choose_name(bot, update):
    state = _states[user(update)]
    print(update.message.text)
    state['name'] = update.message.text
    update.message.reply_text(say.choose_pack_privacy)
    return CHOOSE_PRIVACY


def choose_privacy(bot, update):
    state = _states[user(update)]
    print(update.message.text)
    state['privacy'] = update.message.text

    pack_id = queries.new_pack(state['name'], user(update), state['privacy'])
    update.message.reply_text('Successfully created pack ' + str(pack_id))

    return END

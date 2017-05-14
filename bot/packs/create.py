from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, File
from telegram.ext import ConversationHandler
import say
from utils import user, row_markup
from db import queries
from packs import packfile
from db.enums import *

END = ConversationHandler.END
START = 0
CHOOSE_NAME = 1
CHOOSE_PRIVACY = 2
CHOOSE_PACK_FILE = 3

_states = {}


def start(bot, update):
    _states[user(update)] = {}
    update.message.reply_text(say.choose_pack_name)
    return CHOOSE_NAME


def choose_name(bot, update):
    state = _states[user(update)]
    state['name'] = update.message.text
    update.message.reply_text(say.choose_pack_privacy, reply_markup=row_markup(PrivacyType.values())) # здесь упало при тестах
# reply_markup=row_markup(PrivacyType.value()))
# File
# "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/enum.py", line
# 324, in __getattr__
# raise AttributeError(name) from None
# AttributeError: value
    return CHOOSE_PRIVACY


def choose_privacy(bot, update):
    state = _states[user(update)]
    text = update.message.text

    if not PrivacyType.has(text):
        update.message.reply_text('Wrong privacy type')
        return CHOOSE_PRIVACY

    state['privacy'] = text
    update.message.reply_text(say.upload_pack_file)
    return CHOOSE_PACK_FILE


def choose_pack_file(bot, update):
    state = _states[user(update)]
    file_id = update.message.document.file_id
    # Doesn't support pipe :(
    # TODO: Delete temp file
    bot.getFile(file_id).download('/tmp/learning_cards_' + str(file_id))
    try:
        pack = packfile.load(open('/tmp/learning_cards_' + str(file_id)))
    except packfile.InvalidPack as e:
        update.message.reply_text(say.invalid_pack.format(e.line))
        return CHOOSE_PACK_FILE
    pack = pack if len(pack) < 100 else pack[:100]
    pack = list(set(pack))
    pack_id = queries.new_pack(
        name=state['name'],
        owner=user(update),
        privacy=state['privacy'],
        cards=pack
    )
    update.message.reply_text(say.pack_created.format(pack_id))
    return END

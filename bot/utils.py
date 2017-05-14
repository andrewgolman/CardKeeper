from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

import functools
import logging
from db import queries
import say


def errors_ignore_and_log(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.exception("Error")
    return wrapped


def send(update, text, markup=None):
    if markup:
        update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup([markup], one_time_keyboard=True))
    else:
        update.message.reply_text(text)


def user(update):
    return update.message.from_user.id


inf_const = 2
CHOOSE_PACK, QUIT = tuple(range(2))


def choose_pack(bot, update):
    packs = queries.active_packs(user(update))
    if not packs:
        send(update, say.no_packs_available)
        return QUIT
    send(update, say.enumerated(packs))
    return CHOOSE_PACK


def get_pack_id(update):
    try:
        pack_id = queries.active_packs(update.message.from_user.id)[int(update.message.text) - 1][0]
    except (TypeError, IndexError, ValueError):
        send(update, say.incorrect_input)
        return None
    return pack_id


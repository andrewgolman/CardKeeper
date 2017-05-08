from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

import functools
import logging


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

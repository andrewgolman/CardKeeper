from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
)

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


def row_markup(lst, one_time_keyboard=True):
    return ReplyKeyboardMarkup(
        map(lambda x: [x], lst),
        one_time_keyboard=one_time_keyboard
    )


def column_markup(lst, one_time_keyboard=True):
    return ReplyKeyboardMarkup([lst], one_time_keyboard=one_time_keyboard)


def send(update, text, markup=None, one_time_keyboard=True):
    if markup:
        update.message.reply_text(
            text,
            reply_markup=row_markup(markup, one_time_keyboard)
        )
    else:
        update.message.reply_text(text)


def user(update):
    return update.message.from_user.id

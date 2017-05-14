from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from db import queries
import say
from random import shuffle
from utils import send, user
from user_states import states
from modes import modes
from modes.modes import ConversationStates

ALL = -1


class LearnState:
    def __init__(self, items):
        self.cards = items
        self.language = 0

    def __str__(self):
        res = ""
        for i in enumerate(self.cards):
            res = res + str(i[1]) + ". " + i[2] + "\n"
        return res

    def answer(self, ans=None):
        res = ""
        for i in enumerate(self.cards):
            if ans and i[0]+1 in ans or ans == [ALL]:
                res = res + str(i[0]+1) + ". " + i[1][2 if self.language else 1] + " - " + i[1][1 if self.language else 2] + "\n"
            else:
                res = res + str(i[0]+1) + ". " + i[1][2 if self.language else 1] + "\n"
        return res

    def shuffle(self):
        shuffle(self.cards)


def init_learn(bot, update):
    states[user(update)] = LearnState(states[user(update)])
    return ask(update, [ALL])


def handle(bot, update):
    try:
        n = int(update.message.text)
    except (TypeError, ValueError, IndexError):
        n = None
    return ask(update, [n])


def ask(update, n=None):
    send(update, states[user(update)].answer(n))
    return ConversationStates.LEARN


def show_all(bot, update):
    return ask(update, [ALL])


def card_shuffle(bot, update):
    states[user(update)].shuffle()
    return ask(update)


def change_language(bot, update):
    states[user(update)].language = not states[user(update)].language
    return ask(update)

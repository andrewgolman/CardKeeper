from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from db import queries
import say
from random import shuffle
from utils import send, user

# Handles all updates within learn mode and ConversationHandler learn_ch
# learn_ch = ConversationHandler(
#     entry_points=[CommandHandler("learn", learn.choose_pack)],
#     states={
#             learn.CHOOSE_PACK: [MessageHandler(Filters.text, learn.pack_chosen)]
#             learn.LEARN: [CommandHandler("change_language", learn.change_language),
#                           CommandHandler("shuffle", learn.shuffle),
#                           MessageHandler(Filters.text, learn.handle)
#                           ]
#     },
#     fallbacks=[
#         CommandHandler("quit", learn.destruct(menu.quit)),
#         CommandHandler("menu", learn.destruct(menu.head_menu)),
#         CommandHandler("begin", learn.destruct(menu.begin))
#     ]
# )


CHOOSE_PACK, LEARN = (0, 1)
ALL = -1
learn_state = {}


class LearnState:
    def __init__(self, items):
        self.cards = items
        self.language = 0

    def __str__(self):
        res = ""
        for i in enumerate(self.cards):
            res = res + str(i[1]) + ". " + i[2] + "\n"
        return res

    def answer(self, ans=[]):
        res = ""
        for i in enumerate(self.cards):
            if i[0]-1 in ans or ans == [ALL]:
                res = res + str(i[0]) + ". " + i[1][2 if self.language else 1] + " - " + i[1][1 if self.language else 2] + "\n"
            else:
                res = res + str(i[0]) + ". " + i[1][2 if self.language else 1] + "\n"
        return res

    def shuffle(self):
        shuffle(self.cards)


def choose_pack(bot, update):
    packs = queries.active_packs(update.message.from_user.id)
    if not packs:
        send(update, say.no_packs_available)
        return ConversationHandler.END
    send(update, say.enumerated(packs))
    return CHOOSE_PACK


def pack_chosen(bot, update):
    try:
        pack_id = queries.active_packs(update.message.from_user.id)[int(update.message.text) - 1][0]
    except TypeError or IndexError:
        send(update, say.incorrect_input)
        return choose_pack(bot, update)
    cards = queries.select_cards(user(update), pack_id)
    if not cards:
        send(update, say.pack_is_empty)
        return choose_pack(bot, update)
    learn_state[user(update)] = LearnState(cards)
    return ask(update, [ALL])


def handle(bot, update):
    try:
        n = int(update.message.text)
    except TypeError:
        n = None
    return ask(update, [n])


def ask(update, n):
    send(update, learn_state[user(update)].answer(n))
    return LEARN


def show_all(bot, update):
    return ask(update, [ALL])


def card_shuffle(bot, update):
    learn_state[user(update)].shuffle()
    return ask(bot, update)


def change_language(bot, update):
    learn_state[user(update)].language = not learn_state[user(update)].language
    return ask(bot, update)


def destruct(func):
    def res(bot, update):
        learn_state.pop(user(update))
        return func(bot, update)
    return res

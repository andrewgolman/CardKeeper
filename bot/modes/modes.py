from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from db import queries
import say
import menu
from utils import send, user
import utils
from random import shuffle
from user_states import states


class ConversationStates:
    CHOOSE_MODE, CHOOSE_PACK, QUIT, CHOOSE_REVIEW_TYPE, CHOOSE_LANGUAGE, ITERATE, LEARN, END = tuple(range(8))


def choose_mode(bot, update):
    ways = ["/review - look through all cards",
            "/learn - see all cards together and remember them",
            "/test - here you will have options to choose from",
            "/practice - bot will not give you right answers"]
    menu.send_menu(update, ways, say.begin_legend)
    return ConversationStates.CHOOSE_MODE


def choose_pack(bot, update):
    packs = queries.active_packs(user(update))
    if not packs:
        send(update, say.no_packs_available)
        return ConversationStates.QUIT
    send(update, say.enumerated(packs))
    return ConversationStates.CHOOSE_PACK


def get_pack_id(update):
    try:
        pack_id = queries.active_packs(update.message.from_user.id)[int(update.message.text) - 1][0]
    except (TypeError, IndexError, ValueError):
        send(update, say.incorrect_input)
        return None
    return pack_id


def pack_chosen(bot, update):
    pack_id = get_pack_id(update)
    if not pack_id:
        return choose_pack(bot, update)
    cards = queries.select_cards(user(update), pack_id)
    if not cards:
        send(update, say.pack_is_empty)
        return choose_pack(bot, update)
    states[user(update)] = cards
    return choose_mode(bot, update)

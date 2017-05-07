from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import queries
import utils
import say

CHOOSE_PACK, CHOOSE_REVIEW_TYPE, CHOOSE_LANGUAGE, ITERATE, END = tuple(range(5))

review_types = ["Trust", "Enter"]
review_state = {}


class ReviewState:
    def __init__(self, items):
        self.cards = items
    cards = []
    wrong_answers = []
    type = review_types[0]
    language = 0


def choose_pack(bot, update):
    packs = queries.active_packs(update.message.from_user.id)
    if not packs:
        utils.send(update, say.no_packs_available)
        return ConversationHandler.END
    utils.send(update, say.enumerated(packs))
    return CHOOSE_PACK


def pack_chosen(bot, update):
    try:
        pack_id = queries.active_packs(update.message.from_user.id)[int(update.message.text) - 1][0]
    except TypeError or IndexError:
        utils.send(update, say.incorrect_input)
        return choose_pack(bot, update)
    cards = queries.select_cards(utils.user(update), pack_id)
    if not cards:
        utils.send(update, say.pack_is_empty)
        return choose_pack(bot, update)
    review_state[utils.user(update)] = ReviewState(cards)
    return choose_review_type(bot, update)


def choose_review_type(bot, update):
    utils.send(update, say.choose_type_of_review, markup=[review_types])
    return CHOOSE_REVIEW_TYPE


def review_type_chosen(bot, update):
    if update.message.text not in review_types:
        utils.send(update, say.incorrect_input, markup=[review_types])
        return choose_review_type(bot, update)
    review_state[utils.user(update)].type = update.message.text
    return choose_language(bot, update)


def choose_language(bot, update):
    utils.send(update, say.choose_language(review_state[utils.user(update)].cards[0]))
    return CHOOSE_LANGUAGE


def language_chosen(bot, update):
    if False:
        utils.send(update, say.incorrect_input)
        return choose_language(bot, update)
    review_state[utils.user(update)].language = 0
    return ITERATE


def review_ask(bot, update):
    return ITERATE


def review_check():
    return review_ask


def review_end():
    return ConversationHandler.END


def test_ask():
    return ITERATE


def test_check():
    return review_ask


def practise_ask():
    pass


def practise_end():
    pass
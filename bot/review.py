from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import queries
import say
import menu
from utils import send, user

CHOOSE_PACK, CHOOSE_REVIEW_TYPE, CHOOSE_LANGUAGE, ITERATE, END = tuple(range(5))

review_types = ["Trust", "Enter"]
review_state = {}
languages = ["Front", "Back"]
practise_markup = ["Proceed"]

review_markup = ["Right", "Wrong"]


class ReviewState:
    def __init__(self, items):
        self.cards = items
        self.right_answers = []
        self.wrong_answers = []
        self.type = review_types[0]
        self.language = 0
        self.first_go = True
        self.shuffle()

    def move(self, user_id):
        self.cards = self.wrong_answers
        self.wrong_answers = []
        if self.first_go:
            for i in self.right_answers:
                queries.update_card_data(user_id, i[0], 1)
        for i in self.wrong_answers:
            queries.update_card_data(user_id, i[0], 0)
        self.first_go = False

    # first card bug
    def ask(self):
        return self.cards[1][2 if self.language else 1]

    def answer(self):
        return self.cards[1][1 if self.language else 2]

    def right(self):
        pass

    def wrong(self):
        pass

    def shuffle(self):
        pass

    def next(self):
        return self.cards[1]

    def check(self):
        if True:
            return None
        return self.cards[0][2 if self.language else 1]


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
    review_state[user(update)] = ReviewState(cards)
    return choose_review_type(bot, update)


def choose_review_type(bot, update):
    send(update, say.choose_type_of_review, markup=[review_types])
    return CHOOSE_REVIEW_TYPE


def review_type_chosen(bot, update):
    if update.message.text not in review_types:
        send(update, say.incorrect_input, markup=[review_types])
        return choose_review_type(bot, update)
    review_state[user(update)].type = update.message.text
    return choose_language(bot, update)


def choose_language(bot, update):
    send(update, say.choose_language(review_state[user(update)].cards[0]), markup=languages)
    return CHOOSE_LANGUAGE


def language_chosen(bot, update):
    if update.message.text not in languages:
        send(update, say.incorrect_input)
        return choose_language(bot, update)
    review_state[user(update)].language = (0 if update.message.text == languages[0] else 1)
    return ITERATE


def review_ask(bot, update):
    send(update, review_state[user(update)].next()[2 if review_state[user(update)].language else 1], markup=[review_markup])
    return ITERATE


def review_check(bot, update):
    send(update, review_state[user(update)].next()[1 if review_state[user(update)].language else 2])
    if update.message.text == review_markup[0]:
        review_state[user(update)].right()
    else:
        review_state[user(update)].wrong()
    return review_ask(bot, update)


def test_ask(bot, update):
    test_markup = review_state[user(update)].test_markup()
    send(update, review_state[user(update)].next()[2 if review_state[user(update)].language else 1], markup=[test_markup])
    return ITERATE


def test_check(bot, update):
    true_ans = review_state[user(update)].compare(update.message.text)
    if not true_ans:
        send(update, say.right)
    else:
        send(update, say.wrong(true_ans))
    return test_ask(bot, update)


def practise_ask(bot, update):
    send(update, review_state[user(update)].next()[2 if review_state[user(update)].language else 1], markup=[practise_markup])
    return ITERATE


def end(bot, update):
    if not review_state[user(update)].wrong_answers:
        send(update, say.completed)
        menu.head_menu(bot, update)
        return ConversationHandler.END
    send(update, say.inter_results(review_state[user(update)]))
    review_state[user(update)].move(user(update))
    return ITERATE


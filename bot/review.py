from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import queries
import say
import menu
from utils import send, user
from random import shuffle

CHOOSE_PACK, CHOOSE_REVIEW_TYPE, CHOOSE_LANGUAGE, START_EX, ITERATE, END = tuple(range(6))

review_types = ["Trust", "Enter", "Test", "Practise"]
review_state = {}
languages = ["Front", "Back"]
practise_markup = ["Proceed"]

trust_markup = ["Right", "Wrong"]

# ConversationHandler(
#         entry_points=[CommandHandler("review", review.choose_pack)],
#         states={
#                 review.CHOOSE_PACK: [MessageHandler(Filters.text, review.pack_chosen)],
#                 review.CHOOSE_REVIEW_TYPE: [MessageHandler(Filters.text, review.review_type_chosen)],
#                 review.CHOOSE_LANGUAGE: [MessageHandler(Filters.text, review.language_chosen)],
#                 # commands through regexp
#                 review.ITERATE: [MessageHandler(Filters.text, review.review_ask)],
#                 review.END: [MessageHandler(Filters.text, review.end)]
#         },
#         fallbacks=default_fallbacks
#     )


class ReviewState:
    def __init__(self, items):
        self.cards = items
        self.right_answers = []
        self.wrong_answers = []
        self.type = None
        self.language = 0
        self.first_go = True
        self.last_card = None
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
        self.shuffle()

    def ask(self):
        return self.next()[2 if self.language else 1]

    def answer(self):
        self.last_card = self.next()
        return self.next()[1 if self.language else 2]

    def right(self):
        self.right_answers.append(self.last_card)

    def wrong(self):
        self.wrong_answers.append(self.last_card)

    def shuffle(self):
        shuffle(self.cards)

    def next(self):
        return self.cards[0]

    def compare(self, s):
        answer = self.next()[2 if self.language else 1]
        if s == answer:
            return None
        return answer

    def test_markup(self):
        pass


def choose_pack(bot, update):
    packs = queries.active_packs(user(update))
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
    return START_EX


def init_test_type(bot, update):
    review_state[user(update)].review_type = review_types[2]
    return ask()


def init_practise_type(bot, update):
    review_state[user(update)].review_type = review_types[3]
    return ask()


def ask(bot, update):
    if review_state[user(update)].review_type == review_types[0]:
        opts = review_markup
    elif review_state[user(update)].review_type == review_types[1]:
        opts = None
    elif review_state[user(update)].review_type == review_types[2]:
        opts = review_state[user(update)].test_markup()
    else:
        opts = practise_markup
    send(update, review_state[user(update)].ask(), markup=opts)
    return ITERATE


def check(bot, update):
    true_ans = review_state[user(update)].compare(update.message.text.strip())
    if not true_ans:
        review_state[user(update)].right()
        send(update, say.right)
    else:
        review_state[user(update)].wrong()
        send(update, say.wrong(true_ans))
    if not review_state[user(update)].cards:
        return end(bot, update)
    return ask(bot, update)


# def trust_check(bot, update):
#
#     if ((review_state[user(update)].review_type == review_types[0] and update.message.text == review_markup[0])
#             or (review_state[user(update)].review_type == review_types[1]
#                 and not review_state[user(update)].compare(update.message.text))):
#         review_state[user(update)].right()
#         # class update?
#     else:
#         review_state[user(update)].wrong()
#     if not review_state[user(update)].cards:
#         return end(bot, update)
#     return ask(bot, update)


def end(bot, update):
    if not review_state[user(update)].wrong_answers:
        send(update, say.completed)
        menu.head_menu(bot, update)
        return ConversationHandler.END
    send(update, say.inter_results(review_state[user(update)]))
    review_state[user(update)].move(user(update))
    return ITERATE

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from db import queries
import say
import menu
from utils import send, user
from random import shuffle
from user_states import states

CHOOSE_PACK, CHOOSE_REVIEW_TYPE, CHOOSE_LANGUAGE, QUIT, ITERATE, END = tuple(range(6))

review_types = ["Trust", "Enter", "Test", "Practise"]
languages = ["Front", "Back"]
practise_markup = ["Proceed"]

trust_markup = ["Right", "Wrong", "/change_language"]


class ReviewState:
    def __init__(self, type):
        self.cards = []
        self.right_answers = []
        self.wrong_answers = []
        self.type = type
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
        self.last_card = self.next()
        return self.last_card[2 if self.language else 1]

    def answer(self):
        return self.last_card[1 if self.language else 2]

    def right(self, update):
        send(update, say.right)
        self.right_answers.append(self.next())
        self.cards.pop(0)

    def wrong(self, update, true_ans):
        send(update, say.wrong(true_ans))
        self.wrong_answers.append(self.next())
        self.cards.pop(0)

    def shuffle(self):
        shuffle(self.cards)

    def next(self):
        return self.cards[0]

    def compare(self, s):
        answer = self.last_card[2 if self.language else 1]
        if s == answer:
            return None
        return answer

    def test_markup(self):
        answers = []
        for i in self.cards, self.right_answers, self.wrong_answers:
            answers.append(i[1 if self.language else 2])
        shuffle(answers)
        return shuffle(self.answer() + answers[:2])

    def last_right(self, update):
        send(update, say.last_answer)
        self.right_answers.append(self.last_card)

    def last_wrong(self, update):
        self.wrong_answers.append(self.last_card)


def init_review(bot, update):
    states[user(update)] = ReviewState(review_types[0])
    return choose_pack(bot, update)


def init_test(bot, update):
    states[user(update)] = ReviewState(review_types[2])
    return choose_pack(bot, update)


def init_practise(bot, update):
    states[user(update)] = ReviewState(review_types[3])
    return choose_pack(bot, update)


def choose_pack(bot, update):
    packs = queries.active_packs(user(update))
    if not packs:
        send(update, say.no_packs_available)
        return QUIT
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
    states[user(update)].cards = cards
    return choose_review_type(bot, update) if states[user(update)] == review_types[0] else choose_language(bot, update)


def choose_review_type(bot, update):
    send(update, say.choose_type_of_review, markup=[review_types])
    return CHOOSE_REVIEW_TYPE


def review_type_chosen(bot, update):
    if update.message.text not in review_types:
        send(update, say.incorrect_input, markup=[review_types])
        return choose_review_type(bot, update)
    states[user(update)].type = update.message.text
    return choose_language(bot, update)


def choose_language(bot, update):
    send(update, say.choose_language(states[user(update)].cards[0]), markup=languages)
    return CHOOSE_LANGUAGE


def language_chosen(bot, update):
    if update.message.text not in languages:
        send(update, say.incorrect_input)
        return choose_language(bot, update)
    states[user(update)].language = (0 if update.message.text == languages[0] else 1)
    return ITERATE


def ask(bot, update):
    if states[user(update)].review_type == review_types[0]:
        opts = trust_markup
    elif states[user(update)].review_type == review_types[1]:
        opts = None
    elif states[user(update)].review_type == review_types[2]:
        opts = states[user(update)].test_markup()
    else:
        opts = practise_markup
    send(update, states[user(update)].ask(), markup=opts)
    return ITERATE


def check(bot, update):
    true_ans = states[user(update)].compare(update.message.text.strip())
    if not true_ans:
        states[user(update)].right(update)
    else:
        states[user(update)].wrong(update, true_ans)
    if not states[user(update)].cards:
        return end(bot, update)
    return ask(bot, update)


def trust_check(bot, update):
    if update.message.text == trust_markup[0]:
        states[user(update)].last_right()
    else:
        states[user(update)].last_wrong()
    return ask(bot, update)


def end(bot, update):
    if not states[user(update)].wrong_answers:
        send(update, say.completed)
        review_quit(bot, update)
        return QUIT
    send(update, say.inter_results(states[user(update)]))
    states[user(update)].move(user(update))
    return ITERATE


def change_language(bot, update):
    states[user(update)].language = not states[user(update)].language
    return ask(bot, update)


def review_quit(bot, update):
    states.pop(user(update))
    menu.head_menu(bot, update)
    return ConversationHandler.END

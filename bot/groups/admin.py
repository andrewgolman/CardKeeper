from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from db import queries
import say
import menu
from modes import modes
from modes.modes import choose_pack
from utils import send, user
import utils
from random import shuffle
from user_states import states
from modes.modes import ConversationStates

class AdminHandlerStates:
        MENU, \
        EDIT_PACKS, \
        APPOINT, \
        ACCEPT, \
        INVITE, \
        STATS, \
        EDIT_GROUP = tuple(range(7))


class AdminStates:
    def __init__(self, group_id):
        self.group_id = group_id
        self.user_in_process = None


def admin_menu(bot, update):
    states[user(update)] = AdminStates(states[user(update)])
    pass


def view_stats(bot, update):
    pass
    # запрос к базе данных о состоянии паков группы у юзеров
    # вывод списка юзеров


def accept_users(bot, update):
    users = queries.applied_to_enter(states[user(update)])
    # вывести юзеров
    return ACCEPT_USERS_HANDLE_NAME


def accept_users_handle_name(bot, update):
    # взять имя
    # states[user(update)].user_in_process = user_id
    # markup = принять, отклонить
    return ACCEPT_USERS_HANDLE_STATE


def accept_users_handle_state(bot, update):
    res = update.message.text.strip()
    # get user_id from state
    if res == "Accept":
        queries.make_user(states[user(update)].group_id, states[user(update).user_in_process])
    else:
        queries.reject_user(states[user(update)].group_id, states[user(update).user_in_process])
    return accept_users(bot, update)

def invite(bot, update):
    pass
    # запрос и рекурсия до exit


def invited(bot, update):
    pass


def appoint_admin(bot, update):
    pass
    # введите имя юзера. если есть - запрос, иначе вернуться.


def admin_appointed(bot, update):
    pass


def enter_nickname(bot, update):
    pass

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from db import queries, enums
import say
import menu
from utils import send, user
from user_states import states

GENERAL_GOAL, WEEKLY_GOAL, NOTIFY_LEARN, NOTIFY_STATS = (0, 1, 2, 3)


def start(bot, update):
    user_id = user(update)
    name = update.message.from_user.username
    states[user_id] = [user_id, name]

    if queries.if_registered(user_id):
        send(update, say.hello)
        menu.head_menu(bot, update)
        return ConversationHandler.END

    send(update, say.welcome)
    return general_goal(update)


def general_goal(update):
    send(update, say.choose_general_goal, markup=enums.GenGoalType.values())
    return GENERAL_GOAL


def general_goal_handle(bot, update):
    res = update.message.text
    if res not in enums.GenGoalType.values():
        send(update, say.incorrect_input + say.choose_general_goal, markup=enums.GenGoalType.values())
        return GENERAL_GOAL
    states[user(update)].append(res)
    return weekly_goal(update)


def weekly_goal(update):
    send(update, say.choose_weekly_goal)
    return WEEKLY_GOAL


def weekly_goal_handle(bot, update):
    try:
        res = int(update.message.text)
        if not 1000 > res > 0:
            raise ValueError
    except (TypeError, ValueError):
        send(update, say.incorrect_weekly_goal)
        return WEEKLY_GOAL
    states[user(update)].append(res)
    return notify_learn(update)


def notify_learn(update):
    send(update, say.choose_learn_notifications, markup=enums.NotificationType.values())
    return NOTIFY_LEARN


def notify_learn_handle(bot, update):
    res = update.message.text
    if res not in enums.NotificationType.values():
        send(update, say.incorrect_input + say.choose_learn_notifications, markup=enums.NotificationType.values())
        return NOTIFY_LEARN
    states[user(update)].append(res)
    return notify_stats(update)


def notify_stats(update):
    send(update, say.choose_stats_notifications, markup=enums.NotificationType.values())
    return NOTIFY_STATS


def notify_stats_handle(bot, update):
    res = update.message.text
    if res not in enums.NotificationType.values():
        send(update, say.incorrect_input + say.choose_general_goal, markup=enums.NotificationType.values())
        return NOTIFY_STATS
    states[user(update)].append(res)
    send(update, say.registration_completed)
    menu.head_menu(bot, update)
    queries.add_user(states.pop(user(update)))
    return ConversationHandler.END

#
# def cancel(bot, update):
#     send(update, say.register_to_access)
#     return ConversationHandler.END

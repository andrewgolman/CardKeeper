from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import queries
import say
import utils

GENERAL_GOAL, WEEKLY_GOAL, NOTIFY_LEARN, NOTIFY_STATS = (0, 1, 2, 3)

users_in_process = {}


def start(bot, update):
    user_id = update.message.from_user.id
    name = update.message.from_user.username
    users_in_process[user_id] = [user_id, name]

    if queries.if_registered(user_id):
        utils.send(update, say.hello)
        menu(bot, update)
        return ConversationHandler.END

    utils.send(update, say.welcome)
    utils.send(update, say.choose_general_goal, markup=say.GEN_GOAL_TYPE)
    return GENERAL_GOAL


def general_goal(bot, update):
    general_goal = update.message.text
    if general_goal not in say.GEN_GOAL_TYPE:
        reply_keyboard = [say.GEN_GOAL_TYPE]
        utils.send(update, say.incorrect_input + say.choose_general_goal, markup=say.GEN_GOAL_TYPE)
        return GENERAL_GOAL
    users_in_process[update.message.from_user.id].append(general_goal)
    utils.send(update, say.choose_weekly_goal)
    return WEEKLY_GOAL


def weekly_goal(bot, update):
    weekly_goal = update.message.text
    # можно ли скастовать к integer?
    users_in_process[update.message.from_user.id].append(weekly_goal)
    utils.send(update, say.choose_learn_notifications, markup=say.NOTIFICATION_TYPE)
    return NOTIFY_LEARN


def notify_learn(bot, update):
    notify_learn = update.message.text
    if notify_learn not in say.NOTIFICATION_TYPE:
        utils.send(update, say.incorrect_input + say.choose_learn_notifications, markup=say.NOTIFICATION_TYPE)
        return NOTIFY_LEARN
    users_in_process[update.message.from_user.id].append(notify_learn)
    utils.send(update, say.choose_stats_notifications, markup=say.NOTIFICATION_TYPE)
    return NOTIFY_STATS


def notify_stats(bot, update):
    notify_stats = update.message.text
    if notify_stats not in say.NOTIFICATION_TYPE:
        utils.send(update, say.incorrect_input + say.choose_general_goal, markup=say.NOTIFICATION_TYPE)
        return NOTIFY_STATS
    users_in_process[update.message.from_user.id].append(notify_stats)
    utils.send(update, say.registration_completed)
    menu(bot, update)
    # print(users_in_process[update.message.from_user.id])
    queries.add_user(users_in_process.pop(update.message.from_user.id))
    return ConversationHandler.END

#
# def cancel(bot, update):
#     utils.send(update, say.register_to_access)
#     return ConversationHandler.END


def menu(bot, update):
    ways = ["/begin", "/packs", "/cards", "/groups", "/settings"]
    legend = say.menu_legend
    menu_opts = "\n".join(ways)
    utils.send(update, legend + '\n' + menu_opts)

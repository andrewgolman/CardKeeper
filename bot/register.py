from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import queries
import say

GENERAL_GOAL, WEEKLY_GOAL, NOTIFY_LEARN, NOTIFY_STATS = (0, 1, 2, 3)

users_in_process = {}


def start(bot, update):
    user_id = update.message.from_user.id
    name = update.message.from_user.username
    users_in_process[user_id] = [user_id, name]

    if queries.if_registered(user_id):
        update.message.reply_text(say.hello)
        menu(bot, update)
        return ConversationHandler.END

    update.message.reply_text(say.welcome)

    reply_keyboard = [['Speech', 'Belletristic', 'Science']]
    update.message.reply_text(say.choose_general_goal,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return GENERAL_GOAL


def general_goal(bot, update):
    general_goal = update.message.text
    users_in_process[update.message.from_user.id].append(general_goal)
    update.message.reply_text(say.choose_weekly_goal)
    return WEEKLY_GOAL


def weekly_goal(bot, update):
    weekly_goal = update.message.text
    users_in_process[update.message.from_user.id].append(weekly_goal)
    reply_keyboard = [['Daily', 'Weekly', 'Never']]
    update.message.reply_text(say.choose_learn_notifications,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return NOTIFY_LEARN


def notify_learn(bot, update):
    notify_learn = update.message.text
    users_in_process[update.message.from_user.id].append(notify_learn)
    reply_keyboard = [['Daily', 'Weekly', 'Never']]
    update.message.reply_text(say.choose_stats_notifications,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return NOTIFY_STATS


def notify_stats(bot, update):
    notify_stats = update.message.text
    users_in_process[update.message.from_user.id].append(notify_stats)
    update.message.reply_text(say.registration_completed)
    menu(bot, update)
    print(users_in_process[update.message.from_user.id])
    queries.add_user(users_in_process.pop(update.message.from_user.id))
    return ConversationHandler.END


def cancel(bot, update):
    update.message.reply_text(say.register_to_access)
    return ConversationHandler.END


def menu(bot, update):
    ways = ["/Begin", "/Packs", "/Groups", "/Settings"]
    legend = say.menu_legend
    menu_opts = "\n".join(ways)
    update.message.reply_text(legend + '\n' + menu_opts)

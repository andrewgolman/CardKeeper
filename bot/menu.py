from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import say


def head_menu(bot, update):
    ways = ["/Begin", "/Packs", "/Groups", "/Settings"]
    legend = say.menu_legend
    menu_opts = "\n".join(ways)
    update.message.reply_text(legend + '\n' + menu_opts)


def quit(bot, update):
    pass


def end(bot, update):
    pass


def begin(bot, update):
    ways = ["/review", "/learn", "/test", "/practice"]
    legend = say.begin_legend
    opts = "\n".join(ways)
    update.message.reply_text(legend + '\n' + opts)


def cards(bot, update):
    pass


def admin(bot, update):
    pass


def group_stats(bot, update):
    pass
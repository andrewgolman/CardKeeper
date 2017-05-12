from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import say
from utils import send

def head_menu(bot, update):
    ways = ["/begin", "/packs", "/groups", "/settings"]
    legend = say.menu_legend
    menu_opts = "\n".join(ways)
    update.message.reply_text(legend + '\n' + menu_opts)


def help(bot, update):
    send(update, say.help)

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

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import say
from utils import send


def send_menu(update, ways, legend=""):
    opts = "\n".join(ways)
    update.message.reply_text(legend + '\n' + opts)


def head_menu(bot, update):
    ways = ["/begin - start an exercise",
            "/packs - add or edit packs",
            "/groups - get tasks from groups",
            "/admin - create or manage a group"
            "/settings"]
    send_menu(update, ways, say.menu_legend)


def help(bot, update):
    send(update, say.help)


def groups(bot, update):
    ways = ["/user", "/admin"]
    send_menu(update, ways)


def group_user(bot, update):
    send(update, say.not_implemented)


def admin_menu(bot, update):
    ways = ["/add_pack", "/update_status", "/view_stats", "/invite_users", "/accept_users", "/appoint_admin"]
    send_menu(update, ways)


def group_stats(bot, update):
    pass

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import say

CHOOSE_NAME = 0

def choose_name(bot, update):
    update.message.reply_text(say.not_implemented)
    return ConversationHandler.END

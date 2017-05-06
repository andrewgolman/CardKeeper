from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import queries
import say
import register
import handlers

token = open("token", "r").read().strip()


def main():
    updater = Updater(token=token)
    dp = updater.dispatcher

    dp.add_handler(handlers.menu_h)
    dp.add_handler(handlers.begin_h)
    dp.add_handler(handlers.cards_h)
    dp.add_handler(handlers.admin_h)
    dp.add_handler(handlers.group_stats_h)

    dp.add_handler(handlers.register_ch)
    dp.add_handler(handlers.review_ch)
    dp.add_handler(handlers.learn_ch)
    dp.add_handler(handlers.test_ch)
    dp.add_handler(handlers.practise_ch)
    dp.add_handler(handlers.new_ch)
    dp.add_handler(handlers.edit_ch)
    dp.add_handler(handlers.update_ch)
    dp.add_handler(handlers.groups_ch)
    dp.add_handler(handlers.add_pack_ch)
    dp.add_handler(handlers.appoint_admin_ch)
    dp.add_handler(handlers.accept_users_ch)
    dp.add_handler(handlers.invite_users_ch)

    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()

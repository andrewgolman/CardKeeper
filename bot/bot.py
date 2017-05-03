from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import queries
import say
import register

token = open("token", "r").read()


def menu(bot, update):
    ways = ["/Begin", "/Packs", "/Groups", "/Settings"]
    legend = say.menu_legend
    menu_opts = "\n".join(ways)
    update.message.reply_text(legend + '\n' + menu_opts)


def begin(bot, update):
    update.message.reply_text(say.choose_a_pack)
    queries.display_active_packs()
    menu(bot, update)




def packs(bot, update):
    msg = "This part is coming up soon!"
    update.message.reply_text(msg)
    menu(bot, update)


def groups(bot, update):
    msg = "This part is coming up soon!"
    update.message.reply_text(msg)
    menu(bot, update)


def settings(bot, update):
    msg = "This part is coming up soon!"
    update.message.reply_text(msg)
    menu(bot, update)


def main():
    updater = Updater(token=token)

    dp = updater.dispatcher

    # dp.add_handler(CommandHandler("start", registration))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler("Begin", begin))
    dp.add_handler(CommandHandler("Packs", packs))
    dp.add_handler(CommandHandler("Groups", groups))
    dp.add_handler(CommandHandler("Settings", settings))

    registration_handler = ConversationHandler(
        entry_points=[CommandHandler('start', register.start)],
        states={
            register.GENERAL_GOAL: [MessageHandler(Filters.text, register.general_goal)],
            register.WEEKLY_GOAL: [MessageHandler(Filters.text, register.weekly_goal)],
            register.NOTIFY_LEARN: [MessageHandler(Filters.text, register.notify_learn)],
            register.NOTIFY_STATS: [MessageHandler(Filters.text, register.notify_stats)],
        },
        fallbacks=[CommandHandler('cancel', register.cancel)]
    )
    #
    # exercise_handler = ConversationHandler(
    #     entry_points=[CommandHandler('begin', modes.begin)],
    #     states={
    #         PACK_LIST: [MessageHandler(Filters.text, modes.choose_pack)],
    #         MODE: [MessageHandler(Filters.text, modes.choose_mode)],
    #         LANGUAGE: [MessageHandler(Filters.text, modes.choose_language)],
    #         PROCESS_CARD: [MessageHandler(Filters.text, modes.general_goal)],
    #     }
    # )
    #

    dp.add_handler(registration_handler)

    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import queries
import say
import register
import modes

token = open("token", "r").read()


def menu(bot, update):
    ways = ["/Begin", "/Packs", "/Groups", "/Settings"]
    legend = say.menu_legend
    menu_opts = "\n".join(ways)
    update.message.reply_text(legend + '\n' + menu_opts)


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

    dp.add_handler(CommandHandler("menu", menu))
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

    exercise_handler = ConversationHandler(
        entry_points=[CommandHandler('Begin', modes.begin)],
        states={
            modes.CHOOSE_PACK: [MessageHandler(Filters.text, modes.choose_pack)],
            modes.CHOOSE_MODE: [MessageHandler(Filters.text, modes.choose_mode)],
            modes.CHOOSE_REVIEW_TYPE: [MessageHandler(Filters.text, modes.start_review)],
            modes.START_REVIEW: [MessageHandler(Filters.text, modes.choose_review_type)],
            modes.START_LEARN: [MessageHandler(Filters.text, modes.start_learn)],
            modes.REVIEW: [CommandHandler('Change_language', modes.change_language),
                           CommandHandler('Stats', modes.review.stats),
                           MessageHandler(Filters.text, modes.review.ask)
                           ],
            modes.LEARN: [CommandHandler('Change_language', modes.change_language),
                          CommandHandler('Show_all', modes.learn.show_all),
                          CommandHandler('Shuffle', modes.learn.shuffle),
                          MessageHandler(Filters.text, modes.learn.ask)
                          ],
            modes.START_TRANSLATE: [MessageHandler(Filters.text, modes.translate.init)],
            modes.TRANSLATE: [CommandHandler('Change_language', modes.change_language),
                          MessageHandler(Filters.text, modes.translate.ask)
                          ],
            # отсюда же вызывается транслейт
            # набирать на клавиатуре не даем, как в ревью
            modes.START_TEST: [MessageHandler(Filters.text, modes.test.start_test)],
            #prints message and then calls init lang as review
            modes.TEST: [CommandHandler('Change_language', modes.change_language),
                           CommandHandler('Stats', modes.review.stats),
                           MessageHandler(Filters.text, modes.review.ask_test)
                           ]
        },
        fallbacks=[CommandHandler('End', modes.end)]
    )

    # group_handler = ConversationHandler(
    #     entry_points=[CommandHandler('Groups', groups.begin)]
    #     states={
    #
    #     }
    # )

    dp.add_handler(registration_handler)
    dp.add_handler(exercise_handler)

    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()

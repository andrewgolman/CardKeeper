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

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import menu
import register
import review
import learn
import packs.edit
import packs.create


def unknown(bot, update):
    update.message.reply_text(
        "Message you entered wasn't recognized by bot.\n"
        'Use /help for list of all commands'
    )


unknown_message_h = MessageHandler(None, unknown)


def cancel(bot, update):
    update.message.reply_text('Cancelled current action')
    return ConversationHandler.END


cancel_h = CommandHandler('cancel', cancel)


default_fallbacks = [cancel_h, unknown_message_h]


simple_handlers = [
    CommandHandler("menu", menu.head_menu),
    CommandHandler("begin", menu.begin),
    CommandHandler("cards", menu.cards),
    CommandHandler("menu", menu.admin),
    CommandHandler("group_stats", menu.group_stats)
]

conversation_handlers = [
    ConversationHandler(
        entry_points=[CommandHandler('start', register.start)],
        states={
            register.GENERAL_GOAL: [MessageHandler(Filters.text, register.general_goal)],
            register.WEEKLY_GOAL: [MessageHandler(Filters.text, register.weekly_goal)],
            register.NOTIFY_LEARN: [MessageHandler(Filters.text, register.notify_learn)],
            register.NOTIFY_STATS: [MessageHandler(Filters.text, register.notify_stats)],
        },
        fallbacks=default_fallbacks
    ),

    ConversationHandler(
        entry_points=[CommandHandler("review", review.choose_pack)],
        states={
                # review.CHOOSE_PACK: [MessageHandler(Filters.text, review.pack_chosen)],
                # review.CHOOSE_REVIEW_TYPE: [MessageHandler(Filters.text, review.review_type_chosen)],
                # review.CHOOSE_LANGUAGE: [MessageHandler(Filters.text, review.language_chosen)],
                # # commands through regexp
                # review.ITERATE: [MessageHandler(Filters.text, review.review_ask)],
                # review.END: [MessageHandler(Filters.text, review.end)]
        },
        fallbacks=default_fallbacks
    ),

    ConversationHandler(
        entry_points=[CommandHandler('packs', packs.edit.choose_pack)],
        states={
            packs.edit.CHOOSE_PACK
        },
        fallbacks=default_fallbacks
    ),

    ConversationHandler(
        entry_points=[CommandHandler('new_pack', packs.create.start)],
        states={
            packs.create.CHOOSE_NAME: [MessageHandler(Filters.text, packs.create.choose_name)],
            packs.create.CHOOSE_PRIVACY: [MessageHandler(Filters.text, packs.create.choose_privacy)]
        },
        fallbacks=default_fallbacks
    )
]

# learn_ch = ConversationHandler(
#     entry_points=[CommandHandler("learn", menu.head_menu)],
#     states={
#             learn.START_LEARN: [],
#             learn.LEARN: []
#     },
#     fallbacks=default_fallbacks
# )

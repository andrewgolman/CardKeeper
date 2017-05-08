from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import menu
import register
import review
import learn


def unknown(bot, update):
    update.message.reply_text(
        "Message you entered wasn't recognized by bot.\n"
        'Use /help for list of all commands'
    )


unknown_message_h = MessageHandler(None, unknown)

menu_h = CommandHandler("menu", menu.head_menu)
begin_h = CommandHandler("Begin", menu.begin)
cards_h = CommandHandler("Cards", menu.cards)
admin_h = CommandHandler("menu", menu.admin)
group_stats_h = CommandHandler("group_stats", menu.group_stats)

register_ch = ConversationHandler(
    entry_points=[CommandHandler('start', register.start)],
    states={
        register.GENERAL_GOAL: [MessageHandler(Filters.text, register.general_goal)],
        register.WEEKLY_GOAL: [MessageHandler(Filters.text, register.weekly_goal)],
        register.NOTIFY_LEARN: [MessageHandler(Filters.text, register.notify_learn)],
        register.NOTIFY_STATS: [MessageHandler(Filters.text, register.notify_stats)],
    },
    fallbacks=[]
)

review_ch = ConversationHandler(
    entry_points=[CommandHandler("review", review.choose_pack)],
    states={
            review.CHOOSE_PACK: [MessageHandler(Filters.text, review.pack_chosen)],
            review.CHOOSE_REVIEW_TYPE: [MessageHandler(Filters.text, review.review_type_chosen)],
            review.CHOOSE_LANGUAGE: [MessageHandler(Filters.text, review.language_chosen)],
            # commands through regexp
            review.ITERATE: [MessageHandler(Filters.text, review.review_ask)],
            review.END: [MessageHandler(Filters.text, review.end)]
    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("menu", menu.head_menu),
        CommandHandler("begin", menu.begin)
    ]
)

learn_ch = ConversationHandler(
    entry_points=[CommandHandler("learn", menu.head_menu)],
    states={
            learn.START_LEARN: [],
            learn.LEARN: []
    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("menu", menu.head_menu),
        CommandHandler("begin", menu.begin)
    ]
)

test_ch = ConversationHandler(
    entry_points=[CommandHandler("test", menu.head_menu)],
    states={
            review.CHOOSE_PACK: [],
            review.CHOOSE_LANGUAGE: [],
            review.ITERATE: []
    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("menu", menu.head_menu),
        CommandHandler("begin", menu.begin)
    ]
)

practise_ch = ConversationHandler(
    entry_points=[CommandHandler("practice", menu.head_menu)],
    states={
            review.CHOOSE_PACK: [],
            review.CHOOSE_LANGUAGE: [],
            review.ITERATE: []
    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("menu", menu.head_menu),
        CommandHandler("begin", menu.begin)
    ]
)

new_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

edit_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)
update_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

groups_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

add_pack_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

appoint_admin_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

accept_users_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

invite_users_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[
        CommandHandler("quit", menu.quit),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

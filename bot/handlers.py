from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import menu
import register

menu_h = CommandHandler("menu", menu.head_menu)
begin_h = CommandHandler("menu", menu.begin)
cards_h = CommandHandler("menu", menu.cards)
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
        fallbacks=[CommandHandler('cancel', register.cancel)]
    )

review_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

learn_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

test_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

practise_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

new_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

edit_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)
update_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

groups_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

add_pack_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

appoint_admin_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

accept_users_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)

invite_users_ch = ConversationHandler(
    entry_points=[CommandHandler("", menu.head_menu)],
    states={

    },
    fallbacks=[CommandHandler("quit", menu.quit),
        CommandHandler("cancel", menu.cancel),
        CommandHandler("end", menu.end),
        CommandHandler("begin", menu.begin)
    ]
)
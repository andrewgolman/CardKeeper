import traceback
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, TelegramError
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import menu
import register
import review
import learn
import say
import admin
import groups
import packs.edit
import packs.create
from user_states import states
from utils import user


def destruct(func):
    def res(bot, update):
        try:
            states.pop(user(update))
        except KeyError:
            pass
        return func(bot, update)
    return res


# python-telegram-bot logs non-TelegramError exceptions to ERROR logger
# For TelegramErrors it just displays warning :shrug:
# However, one can only catch TelegramError by specifying error handler
# It's funny though that it will only catch TelegramError s
# Anyway, ... WTF?
def telegram_error_handler(bot, update, err):
    traceback.print_exception(TelegramError, err, None)


def unknown(bot, update):
    update.message.reply_text(say.not_recognized)


def cancel(bot, update):
    update.message.reply_text('Cancelled current action')
    return ConversationHandler.END


def default_fallback_wrapper(func):
    def f(*args, **kwargs):
        func(*args, **kwargs)
        return ConversationHandler.END
    return f


def default_fallbacks(wrap=default_fallback_wrapper):
    return [
            CommandHandler('cancel', wrap(cancel)),
            CommandHandler('quit', wrap(menu.head_menu)),
            CommandHandler('begin', wrap(menu.head_menu)),
            CommandHandler('menu', wrap(menu.head_menu))
            ]

unknown_message_handler = MessageHandler(None, unknown)


admin_handlers = [ConversationHandler(
                                      entry_points=[CommandHandler("add_pack", admin.choose_pack)],
                                      states={admin.CHOOSE_PACK: MessageHandler(Filters.text, admin.pack_chosen)},
                                      fallbacks=default_fallbacks()
                                      ),
                  CommandHandler("view_stats", admin.view_stats),
                  ConversationHandler(
                                      entry_points=[CommandHandler("appoint_admin", admin.enter_nickname)],
                                      states={admin.ITERATE: MessageHandler(Filters.text, admin.admin_appointed)},
                                      fallbacks=default_fallbacks()
                                      ),
                  ConversationHandler(
                                      entry_points=[CommandHandler("accept_users", admin.accept_users)],
                                      states={admin.ITERATE: MessageHandler(Filters.text, admin.user_accepted)},
                                      fallbacks=default_fallbacks()
                                      ),
                  ConversationHandler(
                                      entry_points=[CommandHandler("invite_users", admin.enter_nickname)],
                                      states={admin.ITERATE: MessageHandler(Filters.text, admin.invited)},
                                      fallbacks=default_fallbacks()
                                      )
                  ]

# new_group_handler = ConversationHandler(
#                         entry_points=[CommandHandler("new_group", groups.create)],
#                         states={
#                             # settings
#                         },
#                         fallbacks=default_fallbacks
#                     )




simple_handlers = [
    CommandHandler("menu", menu.head_menu),
    CommandHandler("begin", menu.begin),
    CommandHandler("cards", menu.cards),
    CommandHandler("menu", menu.admin),
    CommandHandler("group_stats", menu.group_stats),
    CommandHandler("help", menu.help)

    # TODO: warn if cancel is used outside of ConversationHandler
    # CommandHandler('cancel', cancel_outside)
]

conversation_handlers = [
    ConversationHandler(
        entry_points=[CommandHandler('start', register.start)],
        states={
            register.GENERAL_GOAL: [MessageHandler(Filters.text, register.general_goal_handle)],
            register.WEEKLY_GOAL: [MessageHandler(Filters.text, register.weekly_goal_handle)],
            register.NOTIFY_LEARN: [MessageHandler(Filters.text, register.notify_learn_handle)],
            register.NOTIFY_STATS: [MessageHandler(Filters.text, register.notify_stats_handle)],
        },
        fallbacks=default_fallbacks()
    ),

    ConversationHandler(
        entry_points=[CommandHandler('packs', packs.edit.start)],
        states={
            packs.edit.CHOOSE_PACK: [MessageHandler(Filters.text, packs.edit.choose_pack)],
            packs.edit.CHOOSE_PACK_ACTION: [MessageHandler(Filters.text, packs.edit.choose_pack_action)],
            packs.edit.EDIT_PACK_NAME: [MessageHandler(Filters.text, packs.edit.edit_pack_name)],
            packs.edit.EDIT_PACK_PRIVACY: [MessageHandler(Filters.text, packs.edit.edit_pack_privacy)],
            packs.edit.DELETE_PACK: [MessageHandler(Filters.text, packs.edit.delete_pack)],
        },
        fallbacks=default_fallbacks()
    ),

    ConversationHandler(
        entry_points=[CommandHandler('new_pack', packs.create.start)],
        states={
            packs.create.CHOOSE_NAME: [MessageHandler(Filters.text, packs.create.choose_name)],
            packs.create.CHOOSE_PRIVACY: [MessageHandler(Filters.text, packs.create.choose_privacy)],
            packs.create.CHOOSE_PACK_FILE: [MessageHandler(Filters.document, packs.create.choose_pack_file)]
        },
        fallbacks=default_fallbacks()
    ),

    ConversationHandler(
        entry_points=[CommandHandler("learn", learn.choose_pack)],
        states={
            learn.CHOOSE_PACK: [MessageHandler(Filters.text, learn.pack_chosen)],
            learn.LEARN: [CommandHandler("change_language", learn.change_language),
                          RegexHandler('^-1$', learn.change_language),
                          CommandHandler("shuffle", learn.card_shuffle),
                          RegexHandler('^-2$', learn.card_shuffle),
                          CommandHandler("show_all", learn.show_all),
                          RegexHandler('^0$', learn.show_all),
                          RegexHandler('[0-9]+', learn.handle)
                          # MessageHandler(Filters.text, learn.handle)
                          ]
        },
        fallbacks=default_fallbacks(destruct)
    ),

    ConversationHandler(
        entry_points=[CommandHandler("review", review.init_review)],
        states={
                review.CHOOSE_PACK: [MessageHandler(Filters.text, review.pack_chosen)],
                review.CHOOSE_REVIEW_TYPE: [MessageHandler(Filters.text, review.review_type_chosen)],
                review.CHOOSE_LANGUAGE: [MessageHandler(Filters.text, review.language_chosen)],
                review.ITERATE: [CommandHandler("change_language", review.change_language),
                                 MessageHandler(Filters.text, review.check)],
                review.END: [MessageHandler(Filters.text, review.end)],
                review.QUIT: [MessageHandler(Filters.text, review.review_quit)]
        },
        fallbacks=default_fallbacks(destruct)
    ),

    ConversationHandler(
        entry_points=[CommandHandler("test", review.init_test)],
        states={
                review.CHOOSE_PACK: [MessageHandler(Filters.text, review.pack_chosen)],
                review.CHOOSE_LANGUAGE: [MessageHandler(Filters.text, review.language_chosen)],
                review.ITERATE: [CommandHandler("change_language", review.change_language),
                                 MessageHandler(Filters.text, review.check)],
                review.END: [MessageHandler(Filters.text, review.end)],
                review.QUIT: [MessageHandler(Filters.text, review.review_quit)]
        },
        fallbacks=default_fallbacks(destruct)
    ),


    ConversationHandler(
        entry_points=[CommandHandler("practice", review.init_practice)],
        states={
                review.CHOOSE_PACK: [MessageHandler(Filters.text, review.pack_chosen)],
                review.CHOOSE_LANGUAGE: [MessageHandler(Filters.text, review.language_chosen)],
                review.ITERATE: [#CommandHandler("change_language", review.change_language),
                                 MessageHandler(Filters.text, review.check)],
                review.END: [MessageHandler(Filters.text, review.end)],
                review.QUIT: [MessageHandler(Filters.text, review.review_quit)]
        },
        fallbacks=default_fallbacks(destruct)
    ),

    # ConversationHandler(
    #     entry_points=[CommandHandler("admin", admin.start)],
    #     states={
    #             admin.CHOOSE_GROUP: [MessageHandler(Filters.text, admin.group_chosen)],
    #             admin.NEW_GROUP: [new_group_handler],
    #             admin.MENU: admin_handlers,
    #     },
    #     fallbacks=default_fallbacks
    # ),
    #
    # ConversationHandler(
    #     entry_points=[CommandHandler("groups", groups.choose_groups)],
    #     states={
    #         groups.CHOOSE_GROUP: [CommandHandler]
    #     }
    # )

]
#
# H admin (choose group or create) - Command handler
# H add pack from existing - Conversation handler (states=choose_pack)
# H view stats - Command handler
# H appoint admin - Conversation handler (states=enter_nickname)
# H accept users - Conversation handler (states=choose from a list)
# H invite users  - Conversation handler (states=enter_nicknames)
# ]

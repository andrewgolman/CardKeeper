import traceback
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, TelegramError
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import menu
import register
from modes import review, learn, modes
import say
from groups import admin, groups
import utils
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
    update.message.reply_text('Cancelled current action',
                              reply_markup=ReplyKeyboardRemove())
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


# new_group_handler = ConversationHandler(
#                         entry_points=[CommandHandler("new_group", groups.create)],
#                         states={
#                             # settings
#                         },
#                         fallbacks=default_fallbacks
#                     )




simple_handlers = [
    CommandHandler("menu", menu.head_menu),
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
            packs.edit.CHOOSE_PACK: [MessageHandler(Filters.text, packs.edit.choose_pack_h)],
            packs.edit.CHOOSE_PACK_ACTION: [MessageHandler(Filters.text, packs.edit.choose_pack_action_h)],
            packs.edit.EDIT_PACK_NAME: [MessageHandler(Filters.text, packs.edit.edit_pack_name_h)],
            packs.edit.EDIT_PACK_PRIVACY: [MessageHandler(Filters.text, packs.edit.edit_pack_privacy_h)],
            packs.edit.EDIT_PACK_STATUS: [MessageHandler(Filters.text, packs.edit.edit_pack_status_h)],
            packs.edit.DELETE_PACK: [MessageHandler(Filters.text, packs.edit.delete_pack_h)],
            packs.edit.CHOOSE_CARD: [MessageHandler(Filters.text, packs.edit.choose_card_h)],
            # packs.edit.CHOOSE_CARD_ACTION: [MessageHandler(Filters.text, packs.edit.choose_card_action_h)],
            # packs.edit.EDIT_CARD_FRONT: [MessageHandler(Filters.text, packs.edit.edit_card_front_h)],
            # packs.edit.EDIT_CARD_BACK: [MessageHandler(Filters.text, packs.edit.edit_card_back_h)],
            # packs.edit.EDIT_CARD_STATUS: [MessageHandler(Filters.text, packs.edit.edit_card_status_h)],
        },
        fallbacks=default_fallbacks()
    ),

    ConversationHandler(
        entry_points=[CommandHandler('new_pack', packs.create.start)],
        states={
            packs.create.CHOOSE_NAME: [MessageHandler(Filters.text, packs.create.choose_name_h)],
            packs.create.CHOOSE_PRIVACY: [MessageHandler(Filters.text, packs.create.choose_privacy_h)],
            packs.create.CHOOSE_PACK_FILE: [MessageHandler(Filters.document, packs.create.choose_pack_file_h)]
        },
        fallbacks=default_fallbacks()
    ),


    ConversationHandler(
        entry_points=[CommandHandler("begin", modes.choose_pack)],
        states={
            modes.ConversationStates.CHOOSE_PACK: [MessageHandler(Filters.text, modes.pack_chosen)],
            modes.ConversationStates.CHOOSE_MODE: [
                CommandHandler("learn", learn.init_learn),
                CommandHandler("review", review.init_review),
                CommandHandler("test", review.init_test),
                CommandHandler("practice", review.init_practice)
            ],
            modes.ConversationStates.CHOOSE_REVIEW_TYPE: [MessageHandler(Filters.text, review.review_type_chosen)],
            modes.ConversationStates.CHOOSE_LANGUAGE: [MessageHandler(Filters.text, review.language_chosen)],
            modes.ConversationStates.ITERATE: [CommandHandler("change_language", review.change_language),
                                 MessageHandler(Filters.text, review.check)],
            modes.ConversationStates.END: [MessageHandler(Filters.text, review.end)],
            modes.ConversationStates.QUIT: [MessageHandler(Filters.text, review.review_quit)],
            modes.ConversationStates.LEARN: [CommandHandler("change_language", learn.change_language),
                          RegexHandler('^-1$', learn.change_language),
                          CommandHandler("shuffle", learn.card_shuffle),
                          RegexHandler('^-2$', learn.card_shuffle),
                          CommandHandler("show_all", learn.show_all),
                          RegexHandler('^0$', learn.show_all),
                          RegexHandler('[0-9]+', learn.handle)
                          # MessageHandler(Filters.text, learn.handle)
                          ]
        },
        fallbacks=default_fallbacks()
    ),




    # ConversationHandler(
    #     entry_points=[CommandHandler("admin", admin.start)],
    #     states={
    #         admin.MENU: [
    #             RegexHandler("^Edit packs$", admin.choose_pack),
    #             RegexHandler("^Appoint admin$", admin.appoint_admin),
    #             RegexHandler("^Accept users$", admin.accept_users),
    #             RegexHandler("^Invite users$", admin.invite),
    #             RegexHandler("^View stats$", admin.view_stats),
    #             RegexHandler("^Edit group", admin.edit),
    #         ],
    #         admin.EDIT_PACKS: [],
    #         admin.APPOINT: [],
    #         admin.ACCEPT: [],
    #         admin.INVITE: [],
    #         admin.STATS: [],
    #         admin.EDIT_GROUP: []
    #     },
    #     fallbacks=default_fallbacks()
    # ),

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

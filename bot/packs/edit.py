from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
import say
from utils import user, row_markup
from db import queries
from db.enums import *

END = ConversationHandler.END
START = 0
CHOOSE_PACK = 1
CHOOSE_PACK_ACTION = 2
EDIT_PACK_NAME = 3
EDIT_PACK_PRIVACY = 4
DELETE_PACK = 5
CHOOSE_CARD = 6


_states = {}


# TODO: Add pages support
def start(bot, update):
    _states[user(update)] = {}
    return choose_pack(bot, update)


def choose_pack(bot, update):
    packs = map(lambda x: str(x[0]) + ': ' + x[1], queries.active_packs(user(update)))
    update.message.reply_text(say.choose_pack, reply_markup=row_markup(packs))
    return CHOOSE_PACK


def choose_pack_h(bot, update):
    state = _states[user(update)]
    colon_ind = update.message.text.find(':')
    try:
        pack_id = int(update.message.text[:colon_ind])
    except ValueError:
        update.message.reply_text('Invalid')
        return CHOOSE_PACK
    state['pack_id'] = pack_id
    return choose_pack_action(bot, update)


def choose_pack_action(bot, update):
    state = _states[user(update)]
    pack_id = state['pack_id']
    pack_info = queries.get_pack(pack_id)

    if not queries.has_pack_read_access(pack_id, user(update)):
        update.message.reply_text(say.access_denied)
        return CHOOSE_PACK

    markup = []
    markup.append(['Do exercise', 'Show cards'])
    if pack_info['owner_id'] == user(update):
        markup.append(['Edit Name', 'Edit privacy', 'Delete pack'])

    update.message.reply_text(
        say.pack_info.format(pack_info['name'], pack_info['privacy']),
        reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True)
    )

    return CHOOSE_PACK_ACTION


def choose_pack_action_h(bot, update):
    state = _states[user(update)]
    text = update.message.text

    if text == 'Edit Name':
        return edit_pack_name(bot, update)

    if text == 'Edit privacy':
        return edit_pack_privacy(bot, update)

    if text == 'Delete pack':
        return delete_pack(bot, update)

    if text == 'Do exercise':
        update.message.reply_text(say.not_implemented)
        return CHOOSE_PACK_ACTION

    if text == 'Show cards':
        return choose_card(bot, update)

    update.message.reply_text(say.not_recognized)
    return CHOOSE_PACK_ACTION


def edit_pack_name(bot, update):
    state = _states[user(update)]
    pack_info = queries.get_pack(state['pack_id'])
    if pack_info['owner_id'] != user(update):
        update.message.reply_text(say.access_denied)
        return CHOOSE_PACK_ACTION
    update.message.reply_text(say.choose_pack_name)
    return EDIT_PACK_NAME


def edit_pack_name_h(bot, update):
    state = _states[user(update)]
    pack_info = queries.get_pack(state['pack_id'])
    if pack_info['owner_id'] != user(update):
        update.message.reply_text(say.access_denied)
        return END
    queries.update_pack_name(state['pack_id'], update.message.text)
    update.message.reply_text(say.pack_name_updated)
    return END


def edit_pack_privacy(bot, update):
    state = _states[user(update)]
    pack_info = queries.get_pack(state['pack_id'])
    if pack_info['owner_id'] != user(update):
        update.message.reply_text(say.access_denied)
        return CHOOSE_PACK_ACTION
    update.message.reply_text(say.choose_pack_privacy, reply_markup=row_markup(PrivacyType.values()))
    return EDIT_PACK_PRIVACY


def edit_pack_privacy_h(bot, update):
    state = _states[user(update)]
    pack_info = queries.get_pack(state['pack_id'])
    text = update.message.text

    if pack_info['owner_id'] != user(update):
        update.message.reply_text(say.access_denied)
        return END
    if not PrivacyType.has(text):
        update.message.reply_text('Wrong privacy type')
        return EDIT_PACK_PRIVACY

    queries.update_pack_privacy(state['pack_id'], text)
    update.message.reply_text(say.pack_privacy_updated)
    return END


def delete_pack(bot, update):
    state = _states[user(update)]
    pack_info = queries.get_pack(state['pack_id'])
    if pack_info['owner_id'] != user(update):
        update.message.reply_text(say.access_denied)
        return CHOOSE_PACK_ACTION
    update.message.reply_text(say.pack_deletion_confirmation_prompt.format(pack_info['name']))
    return DELETE_PACK


def delete_pack_h(bot, update):
    state = _states[user(update)]
    pack_info = queries.get_pack(state['pack_id'])

    if pack_info['owner_id'] != user(update):
        update.message.reply_text(say.access_denied)
        return END
    if update.message.text != say.pack_deletion_confirmation.format(pack_info['name']):
        update.message.reply_text('Cancelled deletion')
        return END

    queries.delete_pack(state['pack_id'])
    update.message.reply_text(say.pack_deleted)
    return END


def choose_card(bot, update):
    state = _states[user(update)]
    cards = queries.get_all_cards_in_pack(state['pack_id'])
    cards_print = ['{}: {} - {} - {}'.format(x['card_id'], x['front'],
                                             x['back'], x['comment'])
                   for x in cards]
    markup = [['Add card(s)', 'Export as file']] + \
             [[x] for x in cards_print]
    update.message.reply_text(
        '\n'.join(cards_print),
        reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True)
    )
    return CHOOSE_CARD


def choose_card_h(bot, update):
    update.message.reply_text(say.not_implemented)
    return END

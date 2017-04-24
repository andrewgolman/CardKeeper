from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token = open("token", "r").read()


def make_command(s):
    return '/' + s


def if_registered(user_id):
    return False
    # query expected


def registration(bot, update):
    user_id = update.message.from_user
    if if_registered(user_id):
        update.message.reply_text("already registered")
    # get more info and sent to a database


def menu(bot, update):
    ways = ["Begin", "Packs", "Groups", "Settings"]
    legend = "MENU"
    menu_opts = "\n".join(map(make_command, ways))
    update.message.reply_text(legend + '\n' + menu_opts)


def begin(bot, update):
    msg = "This part is coming up soon!"
    update.message.reply_text(msg)
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

    dp.add_handler(CommandHandler("start", registration))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler("Begin", begin))
    dp.add_handler(CommandHandler("Packs", packs))
    dp.add_handler(CommandHandler("Groups", groups))
    dp.add_handler(CommandHandler("Settings", settings))


    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()

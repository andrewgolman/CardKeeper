# Learning_Cards
Databases course project

by Andrew Golman, Roman Nikonov

## Try

### Hosted

Bot is available at t.me/CardKeeperBot when run. You can register and try some modes, help messages are coming up.

### Run yourself

If you want to run bot yourself, you need to use Python 3 and install `psycopg2` and `python-telegram-bot`:

    pip3 install psycopg2
    pip3 install python-telegram-bot

Also you should have PostgreSQL database configured according to `bot/queries.py` settings. Finally, run it with

    python3 bot/bot.py

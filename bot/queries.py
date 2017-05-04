import psycopg2

base = psycopg2.connect("dbname='cardkeepersample' user='andrew' host='localhost' password='1234'")
cursor = base.cursor()

# Wrapped queries in alphabetic order


def push():
    cursor.execute("COMMIT;")


def add_user(user):
    query = """INSERT INTO users (user_id, name, general_goal, weekly_goal, notifications_learn, notifications_stats, joined)
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', current_date);""".format(*user)
    cursor.execute(query)
    push()


def active_packs(user_id):
    query = """SELECT packs.pack_id, packs.name FROM user_packs, packs WHERE packs.pack_id = user_packs.pack_id
                AND user_packs.status = 'Active' AND user_id = {} ORDER BY pack_id;""".format(user_id)
    cursor.execute(query)
    return cursor.fetchall()


def if_registered(user):
    query = "SELECT * FROM users WHERE users.user_id = '{}';".format(user)
    cursor.execute(query)
    return True if len(cursor.fetchall()) else False


def if_username_taken(username):
    query = "SELECT * FROM users WHERE users.name = '{}';".format(username)
    cursor.execute(query)
    return True if len(cursor.fetchall()) else False


def cards_for_learning(user_id):
    query = """SELECT cards.front, cards.back, cards.comment FROM user_cards, cards
                WHERE user_cards.card_id = cards.card_id AND
                user_id = {} AND cards.type = 'Short'""".format(user_id)


def new_card(front, back):
    query = "INSERT INTO cards (front, back) VALUES ('{}', '{}');".format(front, back)
    push()
    cursor.execute(query)


def new_pack(name, owner, privacy='public', status='active'):
    query = "INSERT INTO packs (name, owner_id, privacy) VALUES ('{}' '{}' '{}');".format(name, owner, privacy)
    cursor.execute(query)
    push()
    query = "SELECT pack_id FROM packs WHERE name = {} AND owner_id = {};".format(name, owner)
    cursor.execute(query)
    pack_id = cursor.fetchall()[0].pack_id
    query = "INSERT INTO user_packs (user_id, pack_id, status) VALUES ('{}', '{}', '{}'));".format(owner, pack_id, status)
    cursor.execute(query)
    push()
    return pack_id


def select_cards(user_id, pack_id):
    query = """SELECT cards.front, cards.back, cards.comment FROM cards, user_cards
                WHERE cards.card_id = user_cards.card_id AND user_cards.status = 'Active'
                AND cards.pack_id = {} AND user_cards.user_id = {}""".format(user_id, pack_id)
    cursor.execute(query)
    return cursor.fetchall()


def update_card_data(user_id, card_id, answer):
    query = """UPDATE user_cards SET times_reviewed = times_reviewed+1, correct_answers = correct_answers+{}
                WHERE user_id = {} AND card_id = {}""".format(answer, user_id, card_id)
    cursor.execute(query)
    return cursor.fetchall()


def update_card_status(user_id, card_id, status):
    query = """UPDATE user_cards SET status = '{}'
                WHERE user_id = {} AND card_id = {}""".format(status, user_id, card_id)


def update_pack_status(user_id, pack_id, status):
    query = """UPDATE user_cards SET status = '{}'
                WHERE user_id = {} AND card_id = {}""".format(status, user_id, pack_id)
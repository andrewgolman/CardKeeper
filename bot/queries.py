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
    packs = cursor.fetchall()
    return packs


def if_registered(user):
    query = "SELECT * FROM users WHERE users.user_id = '{}';".format(user)
    cursor.execute(query)
    return True if len(cursor.fetchall()) else False


def if_username_taken(username):
    query = "SELECT * FROM users WHERE users.name = '{}';".format(username)
    cursor.execute(query)
    return True if len(cursor.fetchall()) else False


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

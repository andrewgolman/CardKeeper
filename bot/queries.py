import psycopg2

base = psycopg2.connect("dbname='cardkeepersample' user='andrew' host='localhost' password='1234'")
cursor = base.cursor()


def if_registered(user):
    query = "SELECT * FROM users WHERE users.user_id = '{}'".format(user)
    cursor.execute(query)
    return True if len(cursor.fetchall()) else False


def if_username_taken(username):
    query = "SELECT * FROM users WHERE users.name = '{}'".format(username)
    cursor.execute(query)
    return True if len(cursor.fetchall()) else False


def new_pack(name, owner, privacy='public'):
    query = "INSERT INTO packs (name, owner_id, privacy) VALUES ('{}' '{}' '{}')".format(name, owner, privacy)
    cursor.execute(query)


def new_card(front, back):
    query = "INSERT INTO cards (front, back) VALUES ('{}', '{}')".format(front, back)
    cursor.execute(query)

def display_active_packs(user_id):
    pass
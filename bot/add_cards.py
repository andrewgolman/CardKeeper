from db import queries

formats = ["", ".txt", ".doc"]


class Cardtype:
    def __init__(self, s):
        s = s.replace("- ", "\t")
        s = s.split("\t")
        self.front = s[0].strip()
        self.back = s[1].strip() if len(s) > 1 else ""

    def side(self, b):
        return self.front if b else self.back


def miss_line(s):
    if s[0] == "/":
        return True
    for c in s:
        if not c.isspace():
            return False
    return True


def get_pack_from_file(file):
    lines = None
    for f in formats:
        try:
            lines = open(file+f, "r").readlines()
        except OSError:
            pass
    cards = []
    if lines:
        for l in lines:
            if l[0] == '!':
                break
            if not miss_line(l):
                cards.append(Cardtype(l))
    return cards


def add_from_file(file):
    cards = get_pack_from_file(file)
    queries.new_pack(file)
    for card in cards:
        queries.new_card(card)

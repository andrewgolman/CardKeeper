formats = ["", ".txt", ".doc"]


class Cardtype:
    def __init__(self, s):
        s = s.replace("- ", "\t")
        self.front = s.split("\t")[0].strip()
        try:
            self.back = s.split("\t")[1].strip()
        except IndexError:
            self.back = ""

    def side(self, b):
        return self.front if b else self.back


def miss_line(s):
    if s[0] == "/":
        return True
    for c in s:
        if not c.isspace():
            return False
    return True


def get_pack(file):
    lines = None
    for f in formats:
        try:
            lines = open(file+f, "r").readlines()
        except OSError:
            pass
    if not lines:
        return None
    cards = []
    for l in lines:
        if l[0] == '!':
            break
        if not miss_line(l):
            cards.append(Cardtype(l))
    return cards

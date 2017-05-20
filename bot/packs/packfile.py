class InvalidPack(Exception):
    def __init__(self, line):
        super().__init__('Invalid pack at line ' + str(line))
        self.line = line


def load(f):
    with f:
        was = set()
        ans = []
        i = 1
        for ln in f:
            if len(ln) != 0 and ln[0] != '#':
                ln = ln.replace('- ', ':')
                ln = ln.replace('\t', ':')

                tokens = list(ln.split(':'))
                if len(tokens) == 1:
                    tokens.append(None)
                if len(tokens) == 2:
                    tokens.append(None)
                if len(tokens) != 3:
                    raise InvalidPack(i)
                if tuple(tokens) in was:
                    continue  # Ignoring this card
                was.add(tuple(tokens))
                front, back, comment = \
                    map(lambda x: x.strip() if x is not None else None, tokens)
                ans.append({'front': front, 'back': back, 'comment': comment})
            i += 1
        return ans


def save(f, pack):
    with f:
        f.write('# Learning_Cards Pack v0.1\n\n')
        for card in pack:
            # TODO: None handling
            front = card['front']
            back = card['back']
            comment = card['comment']
            f.write('{} - {} - {}\n'.format(front, back, comment))
        f.close()

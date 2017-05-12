class InvalidPack(Exception):
    def __init__(self, line):
        super().__init__('Invalid pack at line ' + str(line))
        self.line = line


def load(f):
    with f:
        ans = []
        i = 1
        for ln in f:
            if len(ln) != 0 and ln[0] != '#':
                ln = ln.replace('- ', ':')
                ln = ln.replace('\t', ':')

                tokens = ln.split(':')
                if len(tokens) != 2:
                    raise InvalidPack(i)
                ans.append(tuple(map(lambda x: x.strip(), tokens)))
            i += 1
        return ans


def save(f, pack):
    with f:
        f.write('# Learning_Cards Pack v0.1\n\n')
        for front, back in pack:
            f.write(front + ' - ' + back + '\n')
        f.close()

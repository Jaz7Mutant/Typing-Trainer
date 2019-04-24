class StringBuilder(list):
    def __init__(self):
        super().__init__()
        self._word = []

    def __str__(self):
        return ''.join(self._word)

    def __len__(self):
        return len(self._word)

    def __add__(self, other):
        self._word.append(other)

    def remove_last(self):
        self._word.pop()


INACTIVE_KEYS = [b'\r']
EXIT_KEY = b'\x1b'
ANSWER_YES = [b'\xad', b'\x8d', b'y', b'Y']
ANSWER_NO = [b'\xe2', b'\x92', b'n', b'N']


def highlight_word(word: str):
    return '\x1b[4;35m' + word + '\x1b[0m'


def highlight_word_in_line(line: str, index: int):
    words = line.split(' ')
    words[index] = highlight_word(words[index])
    return ' '.join(words)


def highlight_symbol(symbol: str):
    return '\x1b[4;31m' + symbol + '\x1b[0m'

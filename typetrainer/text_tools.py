class StringBuilder(list):

    def __init__(self):
        super().__init__()
        self.word = []
    # TODO сделать _word

    def add(self, word: str):
        self.word.append(word)

    def remove_last(self):
        self.word.pop()

    def to_string(self):
        return ''.join(self.word)
    # TODO Заменить на __str__, добавить __len__, __add__


def highlight_word(word: str):
    return '\x1b[4;35m' + word + '\x1b[0m'


def highlight_word_in_line(line: str, index: int):
    words = line.split(' ')
    words[index] = highlight_word(words[index])
    return ' '.join(words)


def highlight_symbol(symbol: str):
    return '\x1b[4;31m' + symbol + '\x1b[0m'

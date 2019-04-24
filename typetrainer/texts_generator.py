import random
from typetrainer import menu


class TextGenerator:
    def __init__(self):
        self.config = menu.get_settings()

    def get_random_texts(self, filename: str, text_number: int):
        try:
            with open(filename,
                      encoding=self.config['GENERAL']['FILE_ENCODING']) as f:
                data = f.read()
                texts = data.split('\n\n')
                if text_number == -1:
                    random.shuffle(texts)
                return texts
        except FileNotFoundError:
            print('Dictionary not found')
            exit(self.config['ERR_CODES']['ERROR_MISSING_FILE'])

    def get_random_words(self, filename: str):
        try:
            with open(filename,
                      encoding=self.config['GENERAL']['FILE_ENCODING']) as f:
                data = f.read()
                texts = data.split('\n\n')
                result = []
                for text in texts:
                    lines = text.split('\n')
                    new_text = []
                    for line in lines:
                        words = line.split(' ')
                        random.shuffle(words)
                        new_text.append(' '.join(words))
                    result.append('\n'.join(new_text))

                return result
        except FileNotFoundError:
            print('Dictionary not found')
            exit(self.config['ERR_CODES']['ERROR_MISSING_FILE'])

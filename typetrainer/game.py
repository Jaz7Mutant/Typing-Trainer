from typetrainer import text_tools
import time
import msvcrt
import os
from typetrainer import texts_generator
from typetrainer import menu
from pygame import mixer

mixer.pre_init(44100, -16, 1, 512)
mixer.init()
KEY_SOUND = mixer.Sound('typetrainer/key.wav')
ERR_SOUND = mixer.Sound('typetrainer/err.wav')
RESULT_SOUND = mixer.Sound('typetrainer/result.wav')


def return_score(statistics):
    return round(statistics[1]*100 - (statistics[1]*statistics[0])*2)


def ask_for_continue():
    print('More? (Y\\N)')
    while True:
        key_pressed = msvcrt.getch()
        if key_pressed == text_tools.EXIT_KEY \
                or key_pressed in text_tools.ANSWER_NO:
            return False
        if key_pressed in text_tools.ANSWER_YES:
            return True


def show_score(statistics):
    print('Mistakes: ', statistics[0])
    print('Symbols per minute:', round(statistics[1]))
    print('Accuracy:', round(statistics[2], 2), '%')


class Game:
    def __init__(self, game_type: str, online: bool, text_number=-1):
        self.game_type = game_type
        self.online = online
        self.text_number = text_number
        self.config = menu.get_settings()

    def start_game(self):
        texts = []
        generator = texts_generator.TextGenerator()
        if self.game_type == 'common_texts':
            texts = generator.get_random_texts(
                self.config['DICTIONARIES']['TEXTS_DICTIONARY'],
                self.text_number)
        if self.game_type == 'random_words':
            texts = generator.get_random_words(
                self.config['DICTIONARIES']['WORDS_DICTIONARY'])
        if self.game_type == 'python':
            texts = generator.get_random_texts(
                self.config['DICTIONARIES']['PYTHON_DICTIONARY'],
                self.text_number)
        if self.text_number != -1:
            texts = [texts[self.text_number], '']
        for text in texts:
            statistics = self.run_round(text)
            os.system('cls')
            if not statistics:
                return
            mixer.Sound.play(RESULT_SOUND)
            if self.online:
                return return_score(statistics)
            show_score(statistics)
            if not ask_for_continue():
                return
        print('That\'s all!')
        time.sleep(1)

    def run_round(self, raw_text: str):
        mistakes = 0
        text = raw_text.split('\n')
        start_time = time.time()
        chars_counter = 0
        for line in text:
            words = line.split()
            index = 0
            for word in words:
                chars_counter += len(word)
                os.system('cls')
                try:
                    mistakes += self.match_user_input(
                        word + ' ',
                        text_tools.highlight_word_in_line(line, index))
                except TypeError:
                    return
                index += 1
        end_time = time.time()
        speed = len(raw_text) / (end_time - start_time + 0.001) * 60
        accuracy = (1 - (mistakes / (chars_counter + 1))) * 100
        return mistakes, speed, accuracy

    def match_user_input(self, expected: str, heading: str):
        current_index = 0
        mistakes = 0
        user_input = text_tools.StringBuilder()
        print(heading)
        while True:
            raw_input = msvcrt.getch()
            mixer.Sound.play(KEY_SOUND)

            if raw_input in text_tools.INACTIVE_KEYS:
                continue
            if raw_input == text_tools.EXIT_KEY:
                return

            start_line = '\r'
            if raw_input == b'\x08':
                if len(user_input) != 0:
                    user_input.remove_last()
                    current_index -= 1
                start_line = '\r\033[K'
            else:
                symbol = raw_input.decode(
                    self.config['GENERAL']['INPUT_ENCODING'])
                if current_index >= len(expected) \
                        or symbol != expected[current_index]:
                    mistakes += 1
                    mixer.Sound.play(ERR_SOUND)
                    user_input + text_tools.highlight_symbol(symbol)
                else:
                    user_input + symbol
                current_index += 1
            print(start_line + str(user_input), end='')

            if str(user_input) == expected:
                return mistakes

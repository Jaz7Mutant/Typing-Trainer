from typetrainer import text_tools
import time
from msvcrt import getch
import os
from typetrainer import texts_generator
from typetrainer import menu


config = menu.get_settings()


def start_game(game_type: str, online: bool, text_number=-1):
    texts = []
    if game_type == 'common_texts':
        texts = texts_generator.get_random_texts(
            config['DICTIONARIES']['TEXTS_DICTIONARY'], text_number)
    if game_type == 'random_words':
        texts = texts_generator.get_random_words(
            config['DICTIONARIES']['WORDS_DICTIONARY'])
    if game_type == 'python':
        texts = texts_generator.get_random_texts(
            config['DICTIONARIES']['PYTHON_DICTIONARY'], text_number)
    if text_number != -1:
        texts = [texts[text_number], '']
    for text in texts:
        statistics = run_round(text)
        os.system('cls')
        if not statistics:
            return
        if online:
            return return_score(statistics)
        show_score(statistics)
        if not ask_for_continue():
            return
    print('That\'s all!')
    time.sleep(1)


def ask_for_continue():
    print('More? (Y\\N)')
    while True:
        key_pressed = getch()
        if key_pressed == text_tools.EXIT_KEY \
                or key_pressed in text_tools.ANSWER_NO:
            return False
        if key_pressed in text_tools.ANSWER_YES:
            return True


def return_score(statistics):
    return round(statistics[1]*100 - (statistics[1]*statistics[0]))


def show_score(statistics):
    # TODO OR NOT TODO: Mistakes percents
    print('Mistakes: ', statistics[0])
    print('Symbols per minute:', round(statistics[1]))


def run_round(raw_text: str):
    mistakes = 0
    text = raw_text.split('\n')
    start_time = time.time()
    for line in text:
        words = line.split()
        index = 0
        for word in words:
            os.system('cls')
            try:
                mistakes += match_user_input(
                    word + ' ',
                    text_tools.highlight_word_in_line(line, index))
            except TypeError:
                return
            index += 1
    end_time = time.time()
    speed = len(raw_text) / (end_time - start_time) * 60
    return mistakes, speed


def match_user_input(expected: str, heading: str):
    current_index = 0
    mistakes = 0
    user_input = text_tools.StringBuilder()
    print(heading)
    while True:
        raw_input = getch()
        if raw_input in text_tools.INACTIVE_KEYS:
            continue
        if raw_input == text_tools.EXIT_KEY:
            return

        start_line = '\r'
        if raw_input == b'\x08':
            if len(user_input.word) != 0:
                user_input.remove_last()
                current_index -= 1
            start_line = '\r\033[K'
        else:
            symbol = raw_input.decode(config['GENERAL']['INPUT_ENCODING'])
            if current_index >= len(expected) \
                    or symbol != expected[current_index]:
                mistakes += 1
                user_input.add(text_tools.highlight_symbol(symbol))
            else:
                user_input.add(symbol)
            current_index += 1
        print(start_line + user_input.to_string(), end='')

        if user_input.to_string() == expected:
            return mistakes

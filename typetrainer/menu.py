import os
from typetrainer import settings
from msvcrt import getch
from typetrainer import game


def get_user_name(change_name: bool):
    if not os.path.exists(r'typetrainer\user_data.txt'):
        open(r'typetrainer\user_data.txt', 'w').close()
    os.system('cls')
    with open(r'typetrainer\user_data.txt', 'r+', encoding='utf-8') as data:
        user = data.read().split('\n')
        if not change_name and os.getlogin() == user[0] and user[1]:
            return user[1]
        data.seek(0)
        data.truncate(0)
        data.write(os.getlogin() + '\n')
        print('Please, input your name')
        name = input()
        data.write(name)
        return name


def main_menu():
    while True:
        user_name = ''
        if user_name == '':
            user_name = get_user_name(False)
        # os.system('cls')
        print('\tTypeTrainer ' + settings.VERSION)
        print('\tWelcome, ' + user_name + '!')
        print('Menu:')
        print('\t1. Start game')
        print('\t2. Change name')
        print('\t3. Help')
        print('\t4. About')
        print('\t5. Exit')
        while True:
            key_pressed = getch()

            if key_pressed == b'1':
                game_types_menu()
                break
            if key_pressed == b'2':
                get_user_name(True)
                break
            if key_pressed == b'3':
                show_help()
                break
            if key_pressed == b'4':
                show_about()
                break
            if key_pressed == b'5':
                exit_game()


def game_types_menu():
    os.system('cls')
    print('Choose game type:')
    print('\t1. Single palyer')
    print('\t2. Multi player')
    print('\t3. Return to main menu')
    while True:
        key_pressed = getch()

        if key_pressed == b'1':
            single_player_modes()
            break
        if key_pressed == b'2':
            # TODO: Добавить мультиплеер
            break
        if key_pressed == b'3':
            return


def single_player_modes():
    os.system('cls')
    print('Choose game mode:')
    print('\t1. Random textes')
    print('\t2. Return to main menu')
    while True:
        key_pressed = getch()

        if key_pressed == b'1':
            game.start_game()
            # TODO Исправить, передавать тип
            break
        if key_pressed == b'2':
            return


def show_help():
    # TODO Здесь будет выводиться справка из файла
    pass


def show_about():
    # TODO ABOUT из файла
    pass


def exit_game():
    print('Bye!')
    exit(0)

import os
from msvcrt import getch
from typetrainer import game
from typetrainer import server
from typetrainer import SocketClient2
import configparser


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


def get_settings():
    config = configparser.ConfigParser()
    config.read(r'typetrainer\settings.ini')
    return config


def main_menu():
    user_name = ''
    config = get_settings()
    while True:
        if user_name == '':
            user_name = get_user_name(False)
        os.system('cls')
        print('\tTypeTrainer ' + config['GENERAL']['VERSION'])
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
                user_name = get_user_name(True)
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
    print('\t1. Single player')
    print('\t2. Multi player')
    print('\t3. Return to main menu')
    while True:
        key_pressed = getch()

        if key_pressed == b'1':
            single_player_modes()
            break
        if key_pressed == b'2':
            os.system('cls')
            SocketClient2.load_multiplayer()
            multi_players_menu()
            break
        if key_pressed == b'3':
            return


def single_player_modes():
    os.system('cls')
    print('\tSingle player\n')
    print('Choose game mode:')
    print('\t1. Common texts')
    print('\t2. Random words')
    print('\t3. Python code')
    print('\t4. Return to main menu')

    while True:
        key_pressed = getch()

        if key_pressed == b'1':
            game.start_game('common_texts', False)
            break
        if key_pressed == b'2':
            game.start_game('random_words', False)
            break
        if key_pressed == b'3':
            game.start_game('python', False)
            break
        if key_pressed == b'4':
            return


def multi_players_menu():
    os.system('cls')
    print('\tMulti player\n')
    print('\t1. Create room')
    print('\t2. Connect to room')
    print('\t3. Return to main menu')
    while True:
        key_pressed = getch()

        if key_pressed == b'1':
            server.create_room()
            break
        if key_pressed == b'2':
            server.browse_rooms()
            break
        if key_pressed == b'3':
            return


def show_help():
    # TODO Здесь будет выводиться справка из файла
    pass


def show_about():
    # TODO ABOUT из файла
    pass


def exit_game():
    print('Bye!')
    SocketClient2.sio.disconnect()
    exit(0)

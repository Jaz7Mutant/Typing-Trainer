import urllib.request
from msvcrt import getch


def lobby_main_menu():
    game_type = ''
    players = 1
    while True:
        print('\tLobby')
        print('Game mode: ' + game_type)
        print('Players: ' + players)
        print('\n\t1. Start game')
        print('\t2. Change game mode')
        print('\t3. Exit lobby')

        while True:
            key_pressed = getch()

            if key_pressed == b'1':
                # TODO
                break
            if key_pressed == b'2':
                change_game_mode()
                break
            if key_pressed == b'3':
                return


def connect_to_lobby():
    # TODO
    pass


def change_game_mode():
    # TODO
    pass


def get_ip():
    return urllib.request.urlopen('http://ip-address.ru/show')\
        .read().decode('utf-8')

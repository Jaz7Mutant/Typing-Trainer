from msvcrt import getch
import os
from typetrainer import SocketClient
from typetrainer import menu
from typetrainer import game
import time


GAME_MODE = 'random_texts'
GAME_START = False


def create_room():
    os.system('cls')
    room_name = input('Input room name: ')
    max_players = input('Set max players count: ')
    password = input('Set password: ')
    SocketClient.room_create(room_name, password, menu.get_user_name(False), max_players)
    lobby(True)


def lobby(leader: bool):
    print('\t' + 'Room: ' + SocketClient.current_room)
    print('\tGame mode: ' + GAME_MODE)
    print('\n1. Players')
    if leader:
        print('2. Change game mode')
        print('3. Start game')
    else:
        print('4. Ready')
    print('\n5. Leave room')
    while True:
        key_pressed = getch()

        if key_pressed == b'1':
            show_players_list()
            continue
        if leader and key_pressed == b'2':
            change_game_mode()
            continue
        if leader and key_pressed == b'3':
            SocketClient.room_start(SocketClient.current_room)
            waiting_for_start()
            break
        if not leader and key_pressed == b'4':
            waiting_for_start()
            break
        if key_pressed == b'5':
            SocketClient.sio.disconnect()
            return


def waiting_for_start():
    os.system('cls')
    print('Waiting for other players...')
    while True:
        if GAME_START:
            os.system('cls')
            print('Ready')
            time.sleep(1)
            print('Set')
            time.sleep(1)
            print('Go!')
            time.sleep(1)
            score = game.start_game(GAME_MODE, True)
            SocketClient.room_score(score)
            time.sleep(1)
            os.system('pause')
            return


def show_players_list():
    pass


def change_game_mode():
    os.system('cls')
    print('Choose game mode:')
    print('\t1. Random texts')
    print('\t2. Random words')
    print('\t3. Python code')
    print('\t4. Crazy')
    print('\t5. Return to lobby')

    while True:
        key_pressed = getch()

        if key_pressed == b'1':
            GAME_MODE = 'random_texts'
            break
        if key_pressed == b'2':
            GAME_MODE ='random_words'
            break
        if key_pressed == b'3':
            GAME_MODE = 'python'
            break
        if key_pressed == b'4':
            GAME_MODE = 'crazy'
            break
        if key_pressed == b'5':
            return
    pass


def browse_rooms():
    SocketClient.room_list()
    time.sleep(1)
    room_number = input('Choose room to connect: ')
    password = input('Password: ')
    try:
        SocketClient.room_join(int(room_number), password, menu.get_user_name(False))
    except Exception:
        return
    print(SocketClient.current_room)
    lobby(False)


from msvcrt import getch
import os
from typetrainer import SocketClient2
from typetrainer import menu
from typetrainer import game
import time


GAME_START = False


def create_room():
    os.system('cls')
    room_name = input('Input room name: ')
    max_players = input('Set max players count: ')
    password = input('Set password: ')
    os.system('cls')
    print('Choose game type:')
    print('1. Common texts')
    print('2. Python')

    while True:
        key_pressed = getch()
        if key_pressed == b'1':
            game_type = 'common_texts'
            break
        if key_pressed == b'2':
            game_type = 'python'
            break
    os.system('cls')
    print('Choose text:')
    print('1. First')
    print('2. Second')
    print('3. Third')
    while True:
        key_pressed = getch()
        if key_pressed == b'1':
            text_number = 1
            break
        if key_pressed == b'2':
            text_number = 2
            break
        if key_pressed == b'3':
            text_number = 3
            break

    SocketClient2.room_create(room_name, password, menu.get_user_name(False),
                              int(max_players), game_type, text_number)
    time.sleep(0.5)
    lobby(True)


def lobby(leader: bool):
    while True:
        os.system('cls')
        print('\tRoom: ' + SocketClient2.current_room_name)
        print('\tGame mode: ' + SocketClient2.current_game_type)
        print('\tText number: ' + str(SocketClient2.current_text_number))
        print('\n1. Players')
        if leader:
            print('2. Start game')
        else:
            print('3. Ready')
        print('\n4. Leave room')
        while True:
            key_pressed = getch()

            if key_pressed == b'1':
                show_players_list()
                break
            if leader and key_pressed == b'2':
                SocketClient2.room_start(SocketClient2.current_room)
                waiting_for_start()
                return
            if not leader and key_pressed == b'3':
                waiting_for_start()
                return
            if key_pressed == b'4':
                SocketClient2.sio.disconnect()
                return


def waiting_for_start():
    os.system('cls')
    while True:
        if GAME_START:
            os.system('cls')
            print('Ready')
            time.sleep(1)
            print('Set')
            time.sleep(1)
            print('Go!')
            time.sleep(1)
            score = game.start_game(
                SocketClient2.current_game_type,
                True,
                text_number=SocketClient2.current_text_number)
            if score is None:
                score = 0
            SocketClient2.room_score(score)
            time.sleep(1)
            os.system('pause')
            return
        else:
            print('Waiting for other players... |', end='\r')
            time.sleep(0.25)
            print('Waiting for other players... /', end='\r')
            time.sleep(0.25)
            print('Waiting for other players... -', end='\r')
            time.sleep(0.25)
            print('Waiting for other players... \\', end='\r')
            time.sleep(0.25)
    # todo try 10 times then disconnect


def show_players_list():
    os.system('cls')
    SocketClient2.room_players()
    getch()


def browse_rooms():
    # TODO Correct passwords
    SocketClient2.room_list()
    time.sleep(1)
    room_number = input('Choose room to connect: ')
    password = input('Password: ')
    SocketClient2.room_join(int(room_number), password,
                            menu.get_user_name(False))

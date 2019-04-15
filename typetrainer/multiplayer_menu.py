from msvcrt import getch
import os
from typetrainer import socket_client
from typetrainer import menu
from typetrainer import game
import time


GAME_START = False
CONNECTION = False
GAME_FINISH = False
WAITING_FOR_RESPONSE = False


def create_room():
    os.system('cls')
    room_name = input('Input room name: ')
    if room_name == '':
        return
    max_players = input('Set max players count: ')
    try:
        int(max_players)
    except ValueError:
        return
    password = input('Set password: ')
    os.system('cls')
    print('Choose game type:')
    print('1. Common texts')
    print('2. Python code')

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
    print('1. Easy')
    print('2. Medium')
    print('3. Hard')
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

    socket_client.room_create(room_name, password, menu.get_user_name(False),
                              int(max_players), game_type, text_number)
    time.sleep(0.5)
    lobby(True)


def lobby(leader: bool):
    while True:
        os.system('cls')
        print('\tRoom: ' + socket_client.current_room_name)
        print('\tGame mode: ' + socket_client.current_game_type)
        print('\tText number: ' + str(socket_client.current_text_number))
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
                socket_client.room_start(socket_client.current_room)
                waiting_for_start()
                return
            if not leader and key_pressed == b'3':
                waiting_for_start()
                return
            if key_pressed == b'4':
                socket_client.sio.disconnect()
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
                socket_client.current_game_type,
                True,
                text_number=socket_client.current_text_number)
            if score is None:
                score = 0
            socket_client.room_score(score)
            print('Please, wait for other players')
            while not GAME_FINISH:
                print('|', end='\r')
                time.sleep(0.5)
                print('-', end='\r')
                time.sleep(0.5)
            getch()
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
    socket_client.room_players()
    getch()


def browse_rooms():
    os.system('cls')
    global WAITING_FOR_RESPONSE
    WAITING_FOR_RESPONSE = True
    socket_client.room_list()
    while WAITING_FOR_RESPONSE:
        time.sleep(0.2)
    if CONNECTION:
        lobby(False)

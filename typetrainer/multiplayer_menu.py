import msvcrt
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
    # TODO print user is down
    password = input('Set password: ')
    os.system('cls')
    print('Choose game type:')
    print('1. Common texts')
    print('2. Python code')

    while True:
        key_pressed = msvcrt.getch()
        if key_pressed == b'1':
            game_type = 'common_texts'
            break
        if key_pressed == b'2':
            game_type = 'python'
            break
    os.system('cls')
    print('Choose text type:')
    print('1. Easy')
    print('2. Medium')
    print('3. Hard')
    while True:
        key_pressed = msvcrt.getch()
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
    while socket_client.current_room_TOKEN == '':
        time.sleep(0.5)
    lobby(True)


def lobby(leader: bool):
    while True:
        os.system('cls')
        print('\tRoom: ' + socket_client.CURRENT_ROOM_NAME)
        print('\tGame mode: ' + socket_client.CURRENT_GAME_TYPE)
        print('\tText complexity: ' + str(socket_client.CURRENT_TEXT_NUMBER))
        print('\n1. Players')
        if leader:
            print('2. Start game')
        else:
            print('3. Ready')
        print('\n4. Leave room')
        while True:
            key_pressed = msvcrt.getch()

            if key_pressed == b'1':
                show_players_list()
                break
            if leader and key_pressed == b'2':
                socket_client.room_start(socket_client.current_room_TOKEN)
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
            new_game = game.Game(socket_client.CURRENT_GAME_TYPE,
                                 True,
                                 text_number=socket_client.CURRENT_TEXT_NUMBER)
            os.system('cls')
            print('Ready')
            time.sleep(1)
            print('Set')
            time.sleep(1)
            print('Go!')
            time.sleep(1)
            score = new_game.start_game()
            if score is None:
                score = 0
            socket_client.room_score(score)
            print('Please, wait for other players')
            while not GAME_FINISH:
                print('|', end='\r')
                time.sleep(0.3)
                print('/', end='\r')
                time.sleep(0.3)
                print('-', end='\r')
                time.sleep(0.3)
                print('\\', end='\r')
                time.sleep(0.3)
            msvcrt.getch()
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


def show_players_list():
    os.system('cls')
    socket_client.room_players()
    msvcrt.getch()


def browse_rooms():
    os.system('cls')
    global WAITING_FOR_RESPONSE
    WAITING_FOR_RESPONSE = True
    socket_client.room_list()
    time.sleep(1)
    while WAITING_FOR_RESPONSE:
        time.sleep(0.2)
        print('hui')
    if CONNECTION:
        lobby(False)

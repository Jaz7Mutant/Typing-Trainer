import socketio
from typetrainer import multiplayer_menu
import os
import time
import threading
from typetrainer import menu


sio = socketio.Client()
Rooms = []
current_room_TOKEN = ''
USER_SCORE = 0
SCOREBOARD = []
CURRENT_ROOM_NAME = ''
CURRENT_GAME_TYPE = ''
CURRENT_TEXT_NUMBER = 1
ROOMS_SHOWED = False
LOADED = False


def load_multiplayer():
    if LOADED:
        return
    first_thread = threading.Thread(target=show_loading)
    second_thread = threading.Thread(target=connect_to_server)
    first_thread.start(), second_thread.start()
    first_thread.join(), second_thread.join()


def connect_to_server():
    sio.connect('https://holyserver.herokuapp.com/')
    global LOADED
    LOADED = True


def show_loading():
    while not LOADED:
        print('Loading |', end='\r')
        time.sleep(0.25)
        print('Loading /', end='\r')
        time.sleep(0.25)
        print('Loading -', end='\r')
        time.sleep(0.25)
        print('Loading \\', end='\r')
        time.sleep(0.25)


def room_create(room_name: str, password: str, user_name: str,
                max_clients: int, game_type: str, text_number: int):
    """
    Запрос на создание комнаты
    :param room_name: Название комнаты
    :param password: Пароль для входа
    :param user_name: Имя создателя
    :param max_clients: Максимум игроков в комнате
    :param game_type: Тип игры
    :param text_number: Номер текста
    """
    sio.emit("create", {'roomname': room_name, 'password': password,
                        'username': user_name, 'maxclients': max_clients,
                        "gametype": game_type, "textnumber": text_number})


@sio.on("created")
def room_created(data):
    """
    Срабатывает при попытке создания комнаты
    :return:
        data['err'] =
            null = Комната успешно создана
            400: int =  Пользователь задал количество человек в комнате <= 0

        data['token']:str =  id созданной комнаты
        data['name']: str = Название комнаты
    """
    if not data['err']:
        global current_room_TOKEN
        current_room_TOKEN = data['token']
        global CURRENT_ROOM_NAME
        CURRENT_ROOM_NAME = data['name']
        global CURRENT_GAME_TYPE
        CURRENT_GAME_TYPE = data['gametype']
        global CURRENT_TEXT_NUMBER
        CURRENT_TEXT_NUMBER = data['textnumber']
    elif data['err'] == 400:
        print("Wrong data")


def room_list():
    """
    Запрашивает список доступных комнат
    """
    global ROOMS_SHOWED
    ROOMS_SHOWED = False
    sio.emit("rooms")
    while not ROOMS_SHOWED:
        time.sleep(0.3)


@sio.on("rooms")
def get_rooms(data):
    """
    Срабатывает при запросе списка комнат
    :return:
        data: array = Список комнат
        data[i] =
            token: str = id комнаты
            name: str = название комнаты
            gametype: str = Тип игры
            textnumber: int = Номер текста
            players: str = Строка в формате
            "Людей в комнате/Максимум людей в комнате"
    """
    global Rooms
    Rooms = data
    counter = 1
    for room in Rooms:
        print('%s. %-10s %-8s' % (counter, room['name'], room['players']))
        counter += 1
    if counter > 1:
        room_number = input('Choose a room to connect: ')
        try:
            int(room_number)
        except ValueError:
            multiplayer_menu.WAITING_FOR_RESPONSE = False
            return
        if int(room_number) >= counter:
            print('Incorrect room')
            time.sleep(0.5)
            multiplayer_menu.WAITING_FOR_RESPONSE = False
            return
        password = input('Password: ')
        room_join(int(room_number) - 1, password, menu.get_user_name(False))
    time.sleep(0.8)
    multiplayer_menu.WAITING_FOR_RESPONSE = False
    global ROOMS_SHOWED
    ROOMS_SHOWED = True


def room_join(index: int, password: str, username: str):
    """
    Запрос на подключение к комнате
    :param index: Номер комнаты в списке
    :param password: Пароль для входа
    :param username: Имя игрока в комнате
    """
    sio.emit("join", {'token': Rooms[index]['token'], 'password': password,
                      'username': username})


@sio.on("joined")
def joined(data):
    """
    Срабатывает при попытке присоедениться к комнате
    :return:
        data['err'] =
            null = Пользователь успешно присоеденился
            400: int = Неверный пароль комнаты
            410: int = Попытка подключения к запущенной комнате
            406: int = Попытка подключения к заполненной комнате

        data['token']: str = id комнаты
        data['roomname']: str = Название комнаты
        data['gametype']: str = Тип игры
        data['textnumber']: int = Номер текста
    """
    if not data['err']:
        global current_room_TOKEN
        current_room_TOKEN = data['token']
        global CURRENT_ROOM_NAME
        CURRENT_ROOM_NAME = data['roomname']
        global CURRENT_GAME_TYPE
        CURRENT_GAME_TYPE = data['gametype']
        global CURRENT_TEXT_NUMBER
        CURRENT_TEXT_NUMBER = data['textnumber']
        multiplayer_menu.GAME_FINISH = False
        multiplayer_menu.CONNECTION = True
    elif data['err'] == 400:
        print("Wrong password")
    elif data['err'] == 410:
        print("Room already started")
    elif data['err'] == 406:
        print("Room is full")


def room_start(current_user_room: str):
    """
    Запрос на начало игры в комнате
    :param current_user_room: id запускаемой комнаты
    """
    sio.emit("start", {'token': current_user_room})


@sio.on("start")
def started(data):
    """
    Срабатывает при попытке запустить комнату
    :return:
        data['err'] =
            null = Игра в комнате успешно запущена
            406: int = Попытка запустить уже запущенную комнату
            401: int = Попытка запуска до входа в комнату

        data['room']: str = id запущенной комнаты (Приходит всем пользователям)
    """
    if not data['err']:
        if data['room'] == current_room_TOKEN:
            multiplayer_menu.GAME_START = True
    elif data['err'] == 406:
        print("Room already started")
    elif data['err'] == 401:
        print("You need to join")


def room_score(points: int):
    """
    Отправляет игровой счет на сервер
    :param points: Счет игрока
    """
    sio.emit("score", {'token': current_room_TOKEN, 'score': points})


@sio.on("end")
def end_game(data):
    """
    Срабатывает при окончании игры:
        1) Все пользователи в комнате отправили результат
        2) Через 15с после того как результат пришел от 10 человек в комнате
    При попытке отправить очки
    :return:
        data['err'] =
            null = Игра успешно завершена
            401: int = Пользователь попытался отправить счет, не вступив в
            комнату

        data['room']: str = id комнаты

        data['SCOREBOARD']: array =
            data['SCOREBOARD'][i] =
                name: str = Имя игрока
                score: int = Счет игрока
                token: str = id игрока
    """
    if not data['err']:
        if data['room'] == current_room_TOKEN:
            global SCOREBOARD
            SCOREBOARD = data['clients']
            sio.disconnect()
            SCOREBOARD = sorted(SCOREBOARD, key=lambda info: info['score'],
                                reverse=True)
            counter = 1
            multiplayer_menu.GAME_FINISH = True
            multiplayer_menu.CONNECTION = False
            multiplayer_menu.GAME_START = False
            os.system('cls')
            print('   %-16s %-8s' % ('Name', 'Score'))
            for player in SCOREBOARD:
                if counter == 1:
                    print('%s. %-16s %-8s WINNER' % (counter,
                                                     player['username'],
                                                     player['score']))
                else:
                    print('%s. %-16s %-8s' % (counter,
                                              player['username'],
                                              player['score']))
                counter += 1
    elif data['err'] == 401:
        print("You need to join")


def room_players():
    """
    Запрашивает список игроков в вашей комнате
    """
    sio.emit("players", {"token": current_room_TOKEN})


@sio.on("players")
def get_players(data):
    """
    Срабатывает при запросе списка игроков в вашей комнате
    :return:
        data['err'] =
            null = Список игроков получен
            401: int = Попытка запроса списка до входа в комнату
        data['players']: array =
            data['players'][i]: str = Имя игрока
    """
    if not data['err']:
        counter = 0
        for player in data['players']:
            if counter == 0:
                print(str(counter) + '. ' + player + ' L')
            else:
                print(str(counter) + '. ' + player)
            counter += 1
    elif data['err'] == 401:
        print("You need to join")
    print('Press any key to return')

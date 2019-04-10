import socketio
from typetrainer import game
from typetrainer import server
import os

sio = socketio.Client() # Инстанс сокета
Rooms = []              # Список доступных комнат
current_room = ""       # Токен комнаты, к которой подключен пользователь
points = 0         # Счет пользователя (Число для тестов)
table = []              # Таблица результатов

# Коннект по URL сервера
print('Loading...')
sio.connect('https://holyserver.herokuapp.com/')


@sio.on("created")
def room_created(data):
    """
    Срабатывает при попытке создания комнаты
    :return:
        data['err'] =
            null = Комната успешно создана
            400: int =  Пользователь задал количество человек в комнате <= 0

        data['token]:str =  id созданной комнаты
    """
    if not data['err']:
        global current_room
        current_room = data['token']
        # print("created")
        # print(current_room)
    elif data['err'] == 400:
        print("Wrong data")


@sio.on("rooms")
def get_rooms(data):
    """
    Срабатывает при запросе списка комнат
    :return:
        data: array = Список комнат
        data[i] =
            token: str = id комнаты
            name: str = название комнаты
            players: str = Строка в формате "Людей в комнате/Максимум людей в комнате"
    """
    global Rooms
    Rooms = data
    counter = 1
    for room in Rooms:
        print('%s. %-10s %-8s' % (counter, room['name'], room['players']))
        counter += 1


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
    """
    if not data['err']:
        global current_room
        current_room = data['token']
        print("joined to", current_room)
    elif data['err'] == 400:
        print("Wrong password")
    elif data['err'] == 410:
        print("Room already started")
    elif data['err'] == 406:
        print("Room is full")


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
        if data['room'] == current_room:
            # print("Start")
            server.GAME_START = True
    elif data['err'] == 406:
        print("Room already started")
    elif data['err'] == 401:
        print("You need to join")


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
            401: int = Пользователь попытался отправить счет, не вступив в комнату

        data['room']: str = id комнаты

        {НЕ ОТСОРТИРОВАНО}
        data['table']: array =
            data['table'][i] =
                name: str = Имя игрока
                score: int = Счет игрока
                token: str = id игрока
    """
    if not data['err']:
        if data['room'] == current_room:
            global table
            table = data['clients']
            sio.disconnect()
            sorted(table, key=lambda info: info['score'])
            counter = 1
            os.system('cls')
            print('   Name       Score')
            for player in table:
                if counter == 1:
                    print('%s. %-10s %-8s WINNER' % (counter, player['username'], player['score']))
                else:
                    print(f'{counter}. {player["username"]} {player["score"]}')
                counter += 1
    elif data['err'] == 401:
        print("You need to join")


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


def room_create(room_name: str, password: str, user_name: str, max_clients: int):
    """
    Запрос на создание комнаты
    :param room_name: Название комнаты
    :param password: Пароль для входа
    :param user_name: Имя создателя
    :param max_clients: Максимум игроков в комнате
    :return:
        Ответ приходит в room_created()
    """
    sio.emit("create", {'roomname': room_name, 'password': password, 'username': user_name, 'maxclients': max_clients})


def room_list():
    """
    Запрашивает список доступных комнат
    :return:
        Ответ приходит в get_rooms()
    """
    sio.emit("rooms")


def room_join(index: int, password: str, username: str):
    """
    Запрос на подключение к комнате
    :param index: Номер комнаты в списке
    :param password: Пароль для входа
    :param username: Имя игрока в комнате
    :return:
        Ответ приходит в joined()
    """
    sio.emit("join", {'token': Rooms[index]['token'], 'password': password, 'username': username})


def room_start(current_room: str):
    """
    Запрос на начало игры в комнате
    :param token: id запускаемой комнаты
    :return:
        Ответ приходит в started
    """
    sio.emit("start", {'token': current_room})


def room_score(points: int):
    """
    Отправляет игровой счет на сервер
    :param points: Счет игрока
    :return:
        Ответ приходит в end_game()
    """
    sio.emit("score", {'token': current_room, 'score': points})


def room_players():
    """
    Запрашивает список игроков в вашей комнате
    :return:
        Ответ приходит в get_players()
    """
    sio.emit("players", {"token": current_room})
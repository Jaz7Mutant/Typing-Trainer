import os
import sys
import colorama
import configparser


config = configparser.ConfigParser()
config.read(r'typetrainer\settings.ini')
try:
    from typetrainer import game, server, SocketClient, text_tools, \
        texts_generator, menu
except Exception as e:
    print('Game modules not found: "{}"'.format(e), file=sys.stderr)
    exit(config['ERR_CODES']['ERROR_MISSING_MODULE'])


def main():
    colorama.init()
    menu.main_menu()
    os.system('pause')


if __name__ == '__main__':
    main()

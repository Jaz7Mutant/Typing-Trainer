import sys
import colorama
import configparser
from pygame import mixer

config = configparser.ConfigParser()
config.read(r'typetrainer\settings.ini')
try:
    from typetrainer import game, multiplayer_menu, socket_client, text_tools,\
        texts_generator, menu
except Exception as e:
    print('Game modules not found: "{}"'.format(e), file=sys.stderr)
    exit(config['ERR_CODES']['ERROR_MISSING_MODULE'])


def main():
    if len(sys.argv) > 1:
        parse_args(sys.argv[1])
    colorama.init()
    mixer.pre_init(44100, -16, 1, 512)
    mixer.init()
    mixer.Sound.play(mixer.Sound('typetrainer/hello.wav'))
    menu.main_menu()


def parse_args(arg: str):
    if arg == '-h' or arg == '--help':
        menu.show_help()
        menu.exit_game()
    else:
        raise KeyError('Incorrect argument', arg)


if __name__ == '__main__':
    main()

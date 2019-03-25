import os
import sys
import colorama


ERROR_MISSING_FILE = 1
ERROR_MISSING_MODULE = 2

try:
    from typetrainer import game, settings, texts_generator, menu
except Exception as e:
    print('Game modules not found: "{}"'.format(e), file=sys.stderr)
    exit(ERROR_MISSING_MODULE)


def main():
    colorama.init()
    menu.main_menu()
    os.system('pause')


if __name__ == '__main__':
    main()

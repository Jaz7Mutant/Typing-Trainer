import os
import sys
import colorama


try:
    from typetrainer import game, settings, texts_generator, menu
except Exception as e:
    print('Game modules not found: "{}"'.format(e), file=sys.stderr)
    exit(settings.ERROR_MISSING_MODULE)


def main():
    colorama.init()
    menu.main_menu()
    os.system('pause')


if __name__ == '__main__':
    main()

import unittest
import sys
import os
from unittest import mock
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from typetrainer import game


class TestGame(unittest.TestCase):

    def test_constructor(self):
        new_game = game.Game('common_texts', False, -1)
        self.assertEqual(new_game.text_number, -1)
        self.assertEqual(new_game.online, False)
        self.assertEqual(new_game.game_type, 'common_texts')
        self.assertIsNotNone(new_game.config)

    def test_user_input(self):
        with mock.patch('msvcrt.getch', lambda *_: b'a'):
            new_game = game.Game('common_texts', False, -1)
            self.assertEqual(new_game.match_user_input('a', ''), 0)

    def test_exit_key(self):
        with mock.patch('msvcrt.getch', lambda *_: b'\x1b'):
            new_game = game.Game('common_texts', False, -1)
            self.assertIsNone(new_game.match_user_input('a', ''))

    def test_round_statistics(self):
        with mock.patch('msvcrt.getch', lambda *_: b' '):
            new_game = game.Game('common_texts', False, -1)
            self.assertEqual(new_game.run_round('')[0], 0)

    def test_ask_for_continue_yes(self):
        with mock.patch('msvcrt.getch', lambda *_: b'y'):
            self.assertEqual(game.ask_for_continue(), True)

    def test_ask_for_continue_no(self):
        with mock.patch('msvcrt.getch', lambda *_: b'n'):
            self.assertEqual(game.ask_for_continue(), False)

    def test_score(self):
        self.assertEqual(game.return_score((12, 324)), 24624)

    def test_run_game_with_exit(self):
        with mock.patch('msvcrt.getch', lambda *_: b'\x1b'):
            new_game = game.Game('common_texts', True, -1)
            self.assertIsNone(new_game.start_game())

    def test_show_statistics(self):
        with mock.patch('builtins.print', lambda *_: ''):
            self.assertIsNone(game.show_score((12, 13, 5)))


if __name__ == '__main__':
    unittest.main()

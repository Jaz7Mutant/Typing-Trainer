import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from typetrainer import text_tools


class TestTextTools(unittest.TestCase):

    def test_highlight_word(self):
        self.assertEqual(text_tools.highlight_word('Test'),
                         '\x1b[4;35mTest\x1b[0m')

    def test_highlight_symbol(self):
        self.assertEqual(text_tools.highlight_symbol('T'),
                         '\x1b[4;31mT\x1b[0m')

    def highlight_word_in_line(self):
        self.assertEqual(text_tools.highlight_word_in_line('T e st', 1),
                         'T \x1b[4;35me\x1b[0m st')


if __name__ == '__main__':
    unittest.main()

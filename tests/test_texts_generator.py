import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from typetrainer import texts_generator


class TestTextsGenerator(unittest.TestCase):

    def test_get_random_texts(self):
        tg = texts_generator.TextGenerator()
        self.assertEqual(tg.get_random_texts('tests/text_example', -1),
                         ['afasdfasdfasdfad'])

    def test_get_random_words(self):
        tg = texts_generator.TextGenerator()
        self.assertEqual(tg.get_random_words('tests/text_example'),
                         ['afasdfasdfasdfad'])


if __name__ == '__main__':
    unittest.main()

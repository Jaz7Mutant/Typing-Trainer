import unittest
import os
from typetrainer import menu


class TestMenu(unittest.TestCase):
    def test_get_user_name(self):
        if not os.path.exists(r'typetrainer\user_data'):
            self.assertEqual(None, menu.get_user_name(False))
        else:
            with open(r'typetrainer\user_data', 'r+',
                      encoding='utf-8') as data:
                user = data.read().split('\n')

            self.assertEqual(user[1], menu.get_user_name(False))

    def test_get_config(self):
        self.assertIsNotNone(menu.get_settings())


if __name__ == '__main__':
    unittest.main()

import unittest
from name_function import get_formatted_name

class NamesTestCase(unittest.TestCase):

    def test_first_last_name(self):
        formatted_name = get_formatted_name("yuan", "cheng")
        self.assertEqual(formatted_name, 'Yuan Cheng')

    def test(self):
        formatted_name = get_formatted_name("yuan", "cheng")
        self.assertEqual(formatted_name, 'Yuan2 Cheng')

if __name__ == '__main__':
    unittest.main()


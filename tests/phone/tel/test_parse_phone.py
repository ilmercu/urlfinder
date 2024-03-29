import unittest

from urlfinder.core.elements.base_element import BaseElement
from urlfinder.core.url_parser import URLParser

class TestParsePhone(unittest.TestCase):
    def test_success_is_phone(self):
        main_url = 'tel: +111111111111'
        url_parser = URLParser(main_url)
        self.assertTrue(url_parser.is_phone())

    def test_fail_no_protocol(self):
        main_url = '+111111111111'
        base_url = 'https://abcaei.asd'
        # invalid phone number is considered an URL so a base_url always exists
        url_parser = URLParser(main_url, base_url)
        self.assertFalse(url_parser.is_phone())

    def test_missing_phone(self):
        main_url = 'tel:'
        with self.assertRaises(AttributeError): 
            URLParser(main_url)

    def test_get_value_with_protocol(self):
        current_phone = '+111111111111'
        main_url = f'tel:{current_phone}'
        url_parser = URLParser(main_url)
        phone = BaseElement(url_parser.get_parts())
        self.assertEqual(phone.get_value(), current_phone)

    def test_get_value_between_square(self):
        current_phone = '[111111111111]'
        main_url = f'tel:{current_phone}'
        url_parser = URLParser(main_url)
        phone = BaseElement(url_parser.get_parts())
        self.assertEqual(phone.get_value(), current_phone[1:-1])

    def test_success_phone_contains_word(self):
        current_phone = '+111111111111'
        main_url = f'tel: {current_phone}test'
        url_parser = URLParser(main_url)
        # invalid phone number is considered an URL so a base_url always exists
        phone = BaseElement(url_parser.get_parts())
        self.assertEqual(phone.get_value(), current_phone)

    def test_get_value_between_multi_square(self):
        current_phone = '[[111111111111]]'
        main_url = f'tel:{current_phone}'
        url_parser = URLParser(main_url)
        phone = BaseElement(url_parser.get_parts())
        self.assertEqual(phone.get_value(), current_phone[2:-2])

    def test_get_value_between_multi_square_and_plus(self):
        current_phone = '+[[111111111111]]'
        main_url = f'tel:{current_phone}'
        url_parser = URLParser(main_url)
        phone = BaseElement(url_parser.get_parts())
        self.assertEqual(phone.get_value(), f'+{current_phone[3:-2]}')

    def test_success_with_minus(self):
        current_phone = '+111-111-111'
        main_url = f'tel:{current_phone}'
        url_parser = URLParser(main_url)
        phone = BaseElement(url_parser.get_parts())
        self.assertEqual(phone.get_value(), current_phone)

    def test_success_with_extension(self):
        current_phone = '123-456-7890p123'
        main_url = f'tel:{current_phone}'
        url_parser = URLParser(main_url)
        phone = BaseElement(url_parser.get_parts())
        self.assertEqual(phone.get_value(), current_phone)
        
if __name__ == '__main__':
    unittest.main()
 
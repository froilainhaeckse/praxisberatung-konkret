# test_scraper.py

import unittest
from scraper import convert_month_to_number, extract_titles

class TestScraper(unittest.TestCase):
    def test_convert_month_to_number(self):
        # Test cases for convert_month_to_number function
        self.assertEqual(convert_month_to_number("Januar"), 1)
        self.assertEqual(convert_month_to_number("Februar"), 2)
        self.assertEqual(convert_month_to_number("Dezember"), 12)

    def test_extract_titles(self):
        # Test cases for extract_title function
        url = "https://praxisberatung.wordpress.com"

        expected_titles = [
            "Herzlich Willkommen",
            "Mein Digitaltipp",
            "Mein Veranstaltungstipp",
            "Mein Veranstaltungstipp",
            "Mein Digitaltipp"
        ]

        actual_titles = extract_titles(url)
        for i in range(len(expected_titles)):
            self.assertEqual(actual_titles[i], expected_titles[i])

if __name__ == "__main__":
    unittest.main()
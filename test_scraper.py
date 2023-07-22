# test_scraper.py

import unittest
from bs4 import BeautifulSoup
from datetime import datetime
from scraper import extract_titles, extract_dates

class TestScraper(unittest.TestCase):

    def test_extract_titles(self):
        # Test cases for extract_title function
        html_content_file = "html_content.txt"

        with open(html_content_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        expected_titles = [
            "Herzlich Willkommen",
            "Mein Digitaltipp",
            "Mein Veranstaltungstipp",
            "Mein Veranstaltungstipp",
            "Mein Digitaltipp"
        ]

        actual_titles = extract_titles(soup)
        for i in range(len(expected_titles)):
            self.assertEqual(actual_titles[i], expected_titles[i])
    
    def test_extract_dates(self):
        # Test cases for extract_title function
        html_content_file = "html_content.txt"

        with open(html_content_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')

        expected_dates = [
            "2012-04-02",
            "2023-06-14",
            "2023-05-20",
            "2023-05-08",
            "2023-04-26"
        ]

        actual_dates = extract_dates(soup)

        # Check if the returned value is a list
        self.assertIsInstance(actual_dates, list)

        # If it's a list of dates, compare each date as datetime objects
        for i in range(len(expected_dates)):
            expected_date_obj = datetime.strptime(expected_dates[i], "%Y-%m-%d")
            actual_date_obj = datetime.strptime(actual_dates[i], "%Y-%m-%d")
            self.assertEqual(actual_date_obj, expected_date_obj)

if __name__ == "__main__":
    unittest.main()
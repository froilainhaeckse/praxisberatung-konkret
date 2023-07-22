# test_scraper.py

import unittest
from datetime import datetime
from scraper import extract_titles, extract_dates

class TestScraper(unittest.TestCase):

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
    
    def test_extract_dates(self):
        # Test cases for extract_title function
        url = "https://praxisberatung.wordpress.com"

        expected_dates = [
            "2012-04-02",
            "2023-06-14",
            "2023-05-20",
            "2023-05-08",
            "2023-04-26"
        ]

        # print(extract_dates(url))
        actual_dates = extract_dates(url)

        # Check if the returned value is a list
        self.assertIsInstance(actual_dates, list)

        # If it's a list of dates, compare each date as datetime objects
        for i in range(len(expected_dates)):
            expected_date_obj = datetime.strptime(expected_dates[i], "%Y-%m-%d")
            actual_date_obj = datetime.strptime(actual_dates[i], "%Y-%m-%d")
            self.assertEqual(actual_date_obj, expected_date_obj)

if __name__ == "__main__":
    unittest.main()
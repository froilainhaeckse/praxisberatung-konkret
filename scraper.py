# scraper.py

import os
import requests
import locale
import re
from bs4 import BeautifulSoup
from datetime import datetime
locale.setlocale(locale.LC_TIME, "de_DE") # german

def extract_titles(post_url):
	# Set source WordPress URL
	wp_url = post_url
	
	# Fetch WordPress page HTML
	response = requests.get(wp_url)
	soup = BeautifulSoup(response.text, 'html.parser')

	h2_tags = soup.find_all('h2')
	post_titles = []

	for h2 in h2_tags:
        # Extract title
		post_title = h2.get_text().strip()

		# Check if the post_title starts with "Mein" or "Herzlich"
		if not (post_title.startswith("Mein") or post_title.startswith("Herzlich")):
			continue
	
		post_titles.append(post_title)

	return post_titles

def extract_dates(post_url):
    # Set source WordPress URL
	wp_url = post_url
	
	# Fetch WordPress page HTML
	response = requests.get(wp_url)
	soup = BeautifulSoup(response.text, 'html.parser')

	p_tags = soup.find_all('p')

	dates_list = []

	for parent_element in p_tags:
		# Extract the date from the first welcome post
		if parent_element == p_tags[0]:
			date = parent_element.find('span', class_='entry-date').get_text()
			formatted_date = datetime.strptime(date, "%d. %B %Y").strftime("%Y-%m-%d")
			dates_list.append(formatted_date)
		else:
			# Extract the day from the first <span> element
			day_element = parent_element.find('span', class_='meta-prep meta-prep-author')
			if day_element == None:
				continue
			if not day_element.get_text().startswith("Veröffentlicht"):
				continue
			
			# Define the regular expression pattern to match the date format, include Mail because of Typo
			date_pattern = r'\d{1,2}\. ?(?:Januar|Februar|März|April|Mai|Mail|Juni|Juli|August|September|Oktober|November|Dezember) \d{4}'
			match = re.search(date_pattern, parent_element.get_text())
			if match:
				extracted_date = match.group()
				# Include Mail because of Typo
				if extracted_date == "09. Mail 2022":
					extracted_date = "09. Mai 2022"
				if extracted_date == "02. Mail 2022":
					extracted_date = "02. Mai 2022"
				try:
					date_obj = datetime.strptime(extracted_date, "%d. %B %Y")
				except ValueError:
					date_obj = datetime.strptime(extracted_date, "%d.%B %Y")
				formatted_date = date_obj.strftime("%Y-%m-%d")
				dates_list.append(formatted_date)
	return dates_list

def generate_markdown_file(post_date, post_title, post_content, post_category):
	# ... (same code as before) ...
	pass

def extract_content(post_url):
	# ... (same code as before) ...
	pass

def scrape_wordpress(url):
	# ... (same code as before) ..
	pass
# scraper.py

import os
import requests
import locale
from bs4 import BeautifulSoup
from datetime import datetime
locale.setlocale(locale.LC_TIME, "de_DE") # german

def convert_month_to_number(month_name):
	return datetime.strptime(month_name, '%B').month

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

def extract_date(month):
	# ... (same code as before) ...
	pass

def generate_markdown_file(post_date, post_title, post_content, post_category):
	# ... (same code as before) ...
	pass

def extract_content(post_url):
	# ... (same code as before) ...
	pass

def scrape_wordpress(url):
	# ... (same code as before) ..
	pass
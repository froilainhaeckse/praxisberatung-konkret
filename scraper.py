# scraper.py

import requests
import locale
import re
from bs4 import BeautifulSoup
from datetime import datetime
locale.setlocale(locale.LC_TIME, "de_DE") # german

def extract_date(date_in_a_string):
	# Define the regular expression pattern to match the date format, include Mail because of Typo
	date_pattern = r'\d{1,2}\. ?(?:Januar|Februar|März|April|Mai|Mail|Juni|Juli|August|September|Oktober|November|Dezember) \d{4}'
	match = re.search(date_pattern, date_in_a_string)
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
		return formatted_date

def extract_data(html_content):
	h2_tags = html_content.find_all('h2')
	consolited_data_list = []
	post_title = ""
	post_date = ""

	for h2_tag in h2_tags:
        # Extract title
		post_title = h2_tag.get_text().strip()

		# Check if the post_title starts with "Mein" or "Herzlich" or "Froh"
		if not (post_title.startswith("Mein") or post_title.startswith("Herzlich") or post_title.startswith("Froh")):
			continue

		p_tag_after_h2 = h2_tag.find_next('p')
		
		post_date_text = ""
		if p_tag_after_h2.get_text().startswith("Veröffentlicht"):
			post_date_text = p_tag_after_h2.get_text()
		else:
			post_date_text = h2_tag.find_next('div').get_text()
		if post_date_text == "Veröffentlicht am 10. Septembers 2019":
			# Typo
			post_date_text = "Veröffentlicht am 10. September 2019"
		if post_date == None or post_date == "" or post_date_text == ".":
			# Extract the date from the first welcome post)
			post_date_text = html_content.find('p').find('span', class_='entry-date').get_text()
		
		post_date = extract_date(post_date_text)
		
		consolited_data_element = {"title": post_title, "date": post_date}
		consolited_data_list.append(consolited_data_element)

	return consolited_data_list

def generate_markdown_files(data):
    content_dir = "content/blog/"
	
    for item in data:
	    generate_markdown_file(content_dir, item["title"], item["date"])

def generate_markdown_file(content_dir, title, date):
	# Set destination folder for Hugo content 
	last_word = title.split()[-1]
	filename = f"{content_dir}{date}_{last_word.lower()}.md"
	markdown_content = f"""---
		title: {title}
		date: {date}
		draft: false
		author: "Margitta Kupler"
		thumbnail: {"'/images/digitalfundstueckmonat.webp'" if last_word == "digitaltipp" else ""}
		headline:
		enabled: false
		background: ""
		---

		<!--more-->

		"""
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(markdown_content)
	return markdown_content

def scrape_wordpress(url):
	# Fetch WordPress page HTML
	response = requests.get(url)
	return BeautifulSoup(response.text, 'html.parser')

if __name__ == "__main__":
    url = "https://praxisberatung.wordpress.com/"
    html_content = scrape_wordpress(url)
    data = extract_data(html_content)
    generate_markdown_files(data)
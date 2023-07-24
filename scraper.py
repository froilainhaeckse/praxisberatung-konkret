# scraper.py

import requests
import locale
import re
import html2text
from bs4 import BeautifulSoup
from datetime import datetime
locale.setlocale(locale.LC_TIME, "de_DE") # german

def extract_date(date_in_a_string):
	# Define the regular expression pattern to match the date format, include Mail because of Typo
	date_pattern = r'\d{1,2}\. ?(?:Januar|Februar|März|April|Mai|Mail|Juni|Juli|August|September|Septembers|Oktober|November|Dezember) \d{4}'
	match = re.search(date_pattern, date_in_a_string)
	if match:
		extracted_date = match.group()
		# Include Mail because of Typo
		if extracted_date == "09. Mail 2022":
			extracted_date = "09. Mai 2022"
		if extracted_date == "02. Mail 2022":
			extracted_date = "02. Mai 2022"
		if extracted_date == "10. Septembers 2019":
			extracted_date = "10. September 2019"
		try:
			date_obj = datetime.strptime(extracted_date, "%d. %B %Y")
		except ValueError:
			date_obj = datetime.strptime(extracted_date, "%d.%B %Y")
		formatted_date = date_obj.strftime("%Y-%m-%d")
		return formatted_date

def extract_data(html_content_list):
	data_dictionary = []
	post_title = ""
	post_date = ""
	for i, html_content in enumerate(html_content_list):
		# remove wordpress footer for last post
		if i == len(html_content_list) - 1:
			html_content = html_content.split("</div>")[0]
		post = BeautifulSoup(html_content, 'html.parser')

		# SET AND REMOVE TITLE
		title_tag_for_post = post.find('h2')
		post_title = title_tag_for_post.get_text()
		if title_tag_for_post:
			title_tag_for_post.extract()  # Removes the first h2 tag from the parse tree
		
		# SET AND REMOVE DATE
		post_date = ""

		first_p_tag_in_post = post.find('p')
		first_div_tag_in_post = post.find('div')
		div_tag_with_specific_class_in_post = post.find('div', class_="exhibition-detail__status")
		if first_p_tag_in_post is not None and first_p_tag_in_post.get_text().startswith("Veröffentlicht"):
			post_date = extract_date(first_p_tag_in_post.get_text())
			first_p_tag_in_post.extract()
		elif first_div_tag_in_post is not None and first_div_tag_in_post.get_text().startswith("Veröffentlicht"):
			post_date = extract_date(first_div_tag_in_post.get_text())
			first_div_tag_in_post.extract()
		elif i == 0:
			# Extract the date from the first welcome post)
			p_tag_for_welcome_post = post.find('p').find('span', class_='entry-date')
			post_date = extract_date(p_tag_for_welcome_post.get_text())
			p_tag_for_welcome_post.extract()
		elif div_tag_with_specific_class_in_post:
			post_date = extract_date(div_tag_with_specific_class_in_post.get_text())
			div_tag_with_specific_class_in_post.extract()
		else:
			print("DATE MISSING")
		
		# CONTENT
		a_tag_with_butterfly_to_remove = post.find('a', class_='single-image-gallery', href="https://praxisberatung.wordpress.com/supervision-mv/pkonkret_schmetterling-2/")
		if a_tag_with_butterfly_to_remove:
			a_tag_with_butterfly_to_remove.extract()  # Removes the <a> tag from the parse tree
		
		stripped_post = str(post)
		markdown_content = html2text.html2text(stripped_post)		
		consolited_data_element = {"title": post_title, "date": post_date, "content": markdown_content}
		data_dictionary.append(consolited_data_element)
		
	return data_dictionary

def generate_markdown_files(data):
    content_dir = "content/blog/"
	
    for item in data:
	    generate_markdown_file(content_dir, item["title"], item["date"], item["content"])
	

def generate_markdown_file(content_dir, title, date, content):
	# Set destination folder for Hugo content 
	last_word = title.split()[-1].lower()
	thumbnail_value = "/images/digitalfundstueckmonat.webp" if last_word == "digitaltipp" else ""
	filename = f"{content_dir}{date}_{last_word.lower()}.md"
	markdown_content = f"""---
title: "{title}"
date: "{date}"
draft: false
author: "Margitta Kupler"
categories: "{last_word}"
thumbnail: "{thumbnail_value}"
headline:
  enabled: false
  background: ""
---

{content}

<!--more-->

"""
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(markdown_content)
	return markdown_content

def scrape_wordpress(url):
	# Fetch WordPress page HTML
	response = requests.get(url)
	# Use regular expressions to split the content based on the specified patterns
	split_pattern = r'<h2><strong>→</strong></h2>|<p><strong>→</strong></p>'
	return re.split(split_pattern, response.text)

if __name__ == "__main__":
    url = "https://praxisberatung.wordpress.com/"
    html_content_list = scrape_wordpress(url)
    data_dictionary = extract_data(html_content_list)
    generate_markdown_files(data_dictionary)
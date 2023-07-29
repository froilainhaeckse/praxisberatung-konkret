# scraper.py

import requests
import locale
import re
import html2text
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
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

		# CATEGORY
		post_category = post_title.split()[-1].lower()
		
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

		span_tag_with_dot = post.find('span', style= "color: #ffffff")
		if span_tag_with_dot is not None and span_tag_with_dot.get_text() == '.':
			span_tag_with_dot.extract()

		# GET LOCAL IMAGE LINKS
		image_tags = post.find_all('img')
		local_image_links = []
		year = post_date[:4]
		month = post_date[5:7]
		img_content_dir = f"/images/{year}"

		# Iterate through each image tag and check for "data-orig-file" attribute
		for image_tag in image_tags:
			if image_tag.has_attr('data-orig-file'):
				alt_text = image_tag['alt']
				img_link = image_tag['data-orig-file']
				image_name_unstripped = img_link.split('/')[-1]
				image_name_stripped = image_name_unstripped.replace(" ", "")
				filename = f"{month}_{post_category}_{image_name_stripped}"
				local_image_links.append(img_link)
				# Parse the image URL to extract the file name
				new_img_path = os.path.join(img_content_dir,filename)
				markdown_image = f"![{alt_text}]({new_img_path})"
				image_tag.replace_with(markdown_image)
			butterfly_to_remove = "https://praxisberatung.files.wordpress.com/2012/03/pkonkret_schmetterling2.jpg"
			digitalfundstueck1_to_remove = "https://praxisberatung.files.wordpress.com/2022/11/digitalfundstueck1.png"
			digitalfundstueck2_to_remove = "https://praxisberatung.files.wordpress.com/2022/11/digitalfundstueckmonat2-1.png"
			if butterfly_to_remove in local_image_links:
				local_image_links.remove(butterfly_to_remove)
			if digitalfundstueck1_to_remove in local_image_links:
				local_image_links.remove(digitalfundstueck1_to_remove)
			if digitalfundstueck2_to_remove in local_image_links:
				local_image_links.remove(digitalfundstueck2_to_remove)


		stripped_post = str(post)
		markdown_content = html2text.html2text(stripped_post)		
		consolited_data_element = {"title": post_title, "date": post_date, "category": post_category, "content": markdown_content, "images": local_image_links}
		data_dictionary.append(consolited_data_element)
	
	return data_dictionary

def generate_files(data):
	for item in data:
		title = item["title"]
		date = item["date"]
		category = item["category"]
		content = item["content"]
		images = item["images"]
		year = date[:4]
		img_content_dir = f"themes/hugo-theme-walden/static/images/{year}"
		post_content_dir = f"content/blog/{year}"
		generate_markdown_file(post_content_dir, title, date, category, content)
		generate_image_files(img_content_dir, date, category, images)

	
def generate_image_files(content_dir, date, category, images):
	# TO DO: only create when there are actually images for that year
	if not os.path.exists(content_dir):
		os.makedirs(content_dir)
	for image_url in images:
		# Extract the image name from the URL
		image_name_unstripped = image_url.split('/')[-1]
		image_name_stripped = image_name_unstripped.replace(" ", "")
		month = date[5:7]
		filename = f"{month}_{category}_{image_name_stripped}"
		# Combine the directory path with the image name to get the full save path
		save_path = os.path.join(content_dir,filename)
		save_images(image_url, save_path)

def save_images(url, path):
	response = requests.get(url, stream=True)
	if response.status_code == 200:
		with open(path, 'wb') as f:
			for chunk in response.iter_content(1024):
				f.write(chunk)
		print(f"Image saved as {path}")
	else:
		print(f"Failed to download image from {url}")

def generate_markdown_file(content_dir, title, date, category, content):
	month = date[5:7]
	month_and_day = date[5:10] #TO DO: change - to _
	if not os.path.exists(content_dir):
		os.makedirs(content_dir)
	thumbnail_value = "/images/digitafundstück_billboard.jpg" if category == "digitaltipp" else ""
	# Set destination folder for Hugo content 
	filename = f"{month}_{category}.md"
	new_filename = f"{month_and_day}_{category}.md"
	markdown_content = f"""---
title: "{title}"
date: "{date}"
draft: false
author: "Margitta Kupler"
categories: "{category}"
tags: [""]
thumbnail: "{thumbnail_value}"
headline:
  enabled: false
  background: ""
---

{content}

<!--more-->

"""
	output_file_path = os.path.join(content_dir,filename)
	
	# Check if the file with the same filename already exists
	while os.path.exists(output_file_path):
    	# Generate a new filename with an incrementing number appended to it
		output_file_path = os.path.join(content_dir, new_filename)

	with open(output_file_path, 'w', encoding='utf-8') as f:
		f.write(markdown_content)
	print(f"File saved as {output_file_path}")
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
    generate_files(data_dictionary)    
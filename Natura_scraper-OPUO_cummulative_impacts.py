import os
import time
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from urllib.parse import urljoin

start_time = time.time()

# URL of the initial page
url = 'https://mingor.gov.hr/ocjena-o-potrebi-procjene-utjecaja-zahvata-na-okolis-opuo-4016/4016'
base_url = 'https://mingor.gov.hr'
#folder where the data will be saved
dir = "cummulative_download"
if not os.path.exists(dir):
    os.mkdir(dir)

# Make a request to the initial page
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all links containing "opuo-postupci" from the initial page
links = soup.find_all('a', href=lambda href: href and 'opuo-postupci' in href)

downloaded_files = []
skipped_files = []

# Iterate over the links
for link in links:
    # Construct the full URL for the link
    full_link = base_url + link['href']

    # Extract the year from the link using a regular expression
    year_match = re.search(r'\d{4}', link['href'])
    year = year_match.group() if year_match else ''
    print(year)
    # Make a request to the link
    response = requests.get(full_link)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    opuo_links = soup.find_all('a', href=lambda href: href and href.startswith(f'/opuo-{year}'))
    #remove duplicates
    opuo_links = set(opuo_links)
    for opuo_link in opuo_links:
        full_link = 'https://mingor.gov.hr' + opuo_link['href']
        response = requests.get(full_link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all links containing "opuo" from the current page
        pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
        # Iterate over the PDF links
        for pdf_link in pdf_links:
            # make a pdf url to download file
            pdf_url = pdf_link["href"]
            pdf_url = urljoin(base_url, pdf_url)

            # Make a file name
            file_name = f'OPUO_{year}_{pdf_link["href"].split("/")[-1]}'
            # Make a request to the PDF link
            if os.path.exists("cummulative_download/" + file_name):
                print(file_name, "already exists, skipping download")
            else:
                try:
                    response = requests.get(pdf_url)
                except requests.exceptions.InvalidSchema and requests.exceptions.ConnectionError:
                    print(f"Error: InvalidSchema or Connection error, skipping file: {file_name}")
                    skipped_files.append(file_name)
                    continue
                with open(os.path.join('cummulative_download', file_name), 'wb') as f:
                    f.write(response.content)
                print(f"{file_name} downloaded.")
            downloaded_files.append(file_name)

        print(f"{link} Process finished in: {time.time() - start_time} seconds")
print(f"Process finished in: {time.time() - start_time} seconds")

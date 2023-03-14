import os
import time
import requests
from bs4 import BeautifulSoup
import re

start_time = time.time()

# URL of the initial page
url = 'https://mingor.gov.hr/ocjena-o-potrebi-procjene-utjecaja-zahvata-na-okolis-opuo-4016/4016'

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

# Iterate over the links
for link in links:
    # Construct the full URL for the link
    full_link = 'https://mingor.gov.hr' + link['href']

    # Make a request to the link
    response = requests.get(full_link)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all links containing "opuo" from the current page
    pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
    print(link)
    print(pdf_links)
    # Iterate over the PDF links
    for pdf_link in pdf_links:
        # Construct the full URL for the PDF link
        full_pdf_link = 'https://mingor.gov.hr' + pdf_link['href']

        # Make a request to the PDF link
        response = requests.get(full_pdf_link)
        print(full_pdf_link)
        # Check if the PDF file contains "rjesenje"
        if 'rjesenje' in response.content.lower():
            # Save the PDF file
            file_name = 'OPUO_' + pdf_link['href'].split('/')[-1]
            with open(os.path.join('cummulative_download', file_name), 'wb') as f:
                f.write(response.content)

    print(f"{link} Process finished in: {time.time() - start_time} seconds")
print(f"Process finished in: {time.time() - start_time} seconds")

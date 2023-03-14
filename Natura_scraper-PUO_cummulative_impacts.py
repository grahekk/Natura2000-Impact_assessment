import os
import time
import requests
from bs4 import BeautifulSoup
import re

start_time = time.time()

# The URL of the page to scrape
url = "https://mingor.gov.hr/o-ministarstvu-1065/djelokrug/uprava-za-procjenu-utjecaja-na-okolis-i-odrzivo-gospodarenje-otpadom-1271/procjena-utjecaja-na-okolis-puo-spuo/procjena-utjecaja-zahvata-na-okolis-puo-4014/4014"
#folder where the data will be saved
dir = "cummulative_download"
if not os.path.exists(dir):
    os.mkdir(dir)

# Send a request to the URL and get the HTML response
response = requests.get(url)

# Parse the HTML response using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all <div> elements that concern "PUO postupci"
regex = re.compile(r"PUO postupci ....")
postupci_divs = soup.find_all("div", class_="faqPitanje", string=regex)

downloaded_files = []
skipped_files = []

for postupak_div in postupci_divs:
    #only "PUO postupci" are scraped
    postupak_div = postupak_div.find_previous_sibling("div", class_="faqOdgovor")
    #all the links to be downloaded
    pdf_links = postupak_div.find_all("a")
    # Loop through each <a> element and download the PDF file
    for pdf_link in pdf_links:
        pdf_url = pdf_link["href"]
        if "rjesenje" in pdf_url:
            pdf_name = pdf_url.split("/")[-1]  # Get the file name from the URL
            # Send a request to the PDF URL and download the file and try-except block
            try:
                pdf_response = requests.get(pdf_url)
            except requests.exceptions.InvalidSchema:
                print(f"Error: InvalidSchema, skipping file: {pdf_name}")
                skipped_files.append(pdf_name)
                continue
            #add the folder to file name
            file_name = f"{dir}\\PUO_{pdf_name}"
            try:
                with open(file_name, "wb") as f:
                    f.write(pdf_response.content)
            except FileNotFoundError:
                print(f"Error: FileNotFoundError, skipping file: {pdf_name}")
                skipped_files.append(pdf_name)


            print(f"{pdf_name} downloaded.")
            downloaded_files.append(pdf_name)

print(f"Process finished in: {time.time() - start_time} seconds")

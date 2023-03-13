import os

import requests
from bs4 import BeautifulSoup


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
postupci_divs = soup.find_all("div", class_="faqOdgovor")

# Loop through each <div> element and find the <a> elements with "data-fileid" attribute
for postupak_div in postupci_divs:
    pdf_links = postupak_div.find_all("a")
    print(pdf_links)

    pdf_links = postupak_div.find_all("a",
                                      {"data-fileid": True, "href": True, "target": "_blank", "title": "PUO rješenje"})
    pdf_links = postupak_div.find_all("a", {"href": "rješenje"})
    #pdf_links = postupak_div.find_all("a")
    print(pdf_links)
    # Loop through each <a> element and download the PDF file
    for pdf_link in pdf_links:
        pdf_url = pdf_link["href"]
        pdf_name = pdf_url.split("/")[-1]  # Get the file name from the URL
        pdf_name = f"cummulative_download\\, {pdf_name}"
        # Send a request to the PDF URL and download the file
        pdf_response = requests.get(pdf_url)
        with open(pdf_name, "wb") as f:
            f.write(pdf_response.content)

        print(f"{pdf_name} downloaded.")

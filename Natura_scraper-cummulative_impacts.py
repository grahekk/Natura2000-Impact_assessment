import requests
from bs4 import BeautifulSoup
import urllib.request

# URL of the page to scrape
url = "https://mingor.gov.hr/o-ministarstvu-1065/djelokrug/uprava-za-procjenu-utjecaja-na-okolis-i-odrzivo-gospodarenje-otpadom-1271/procjena-utjecaja-na-okolis-puo-spuo/procjena-utjecaja-zahvata-na-okolis-puo-4014/4014"

# Make a request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all list items in the HTML that contain the text "PUO rješenje"
li_items = soup.find_all("li", string=lambda text: "PUO rješenje" in str(text))

# Loop through each list item and download the corresponding PDF file
for li_item in li_items:
    # Find the nested link element and get the href attribute
    href = li_item.find("a").get("href")
    # Download the PDF file
    urllib.request.urlretrieve(href, li_item.text.strip() + ".pdf")

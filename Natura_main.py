import os
import pandas as pd
import requests
from Natura_config import *
from Natura_scraper_url import law_scrape
from Natura_formater import find_roi

# first test - is the data available? which natura regions are being assessed?
# scraping the data
#law_scrape(to_scrape)

# natura regions
roi = "Donja Posavina"
find_roi(roi)

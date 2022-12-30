import os
import pandas as pd
import requests
from Natura_config import *
from Natura_scraper_url import law_scrape
from Natura_formater import find_roi
from Natura_reporter import *

# scraping the data
#law_scrape(to_scrape)

# natura regions
roi = "Donja Posavina"
#find_roi(roi)

# report creation
#convert_template('Template.docx','html')
#create_report('Template.html')
report_knit('New_document.html')
import os
import pandas as pd
import requests
from Natura_config import *
from Natura_scraper_url import law_scrape
from Natura_formater import find_roi
from Natura_reporter import *

# scraping the data
law_scrape(to_scrape)

# natura regions
roi = "Gorski kotar i sjeverna Lika"
#find_roi(roi)

# report creation
#convert_template('Template.docx','md')
#create_report('Template.html', 'New_document.html')
#create_report_md('Template.md', 'New_document.md')

#mddocx("New_document.md", "New_document.docx")
#report_knit('New_document.html')
#md_to_docx()
#insert_excel()
#obtain_styles()

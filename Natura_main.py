import os
import pandas as pd
import requests
from Natura_config import *
from Natura_scraper_url import *
from Natura_formater import find_roi
from Natura_reporter import *

# scraping the data
law_scrape(to_scrape)

# natura regions
roi = "Stupnički lug"
get_url_from_natura_links('HR2000589',roi)
#sdf_scrape('HR2000589')
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

import os
import pandas as pd
import requests
from Natura_config import *
from bs4 import BeautifulSoup


# scraping from simple html urls
def law_scrape(scraping_list: list):
    for count, scrape in enumerate(scraping_list):
        print(scrape, dict[scrape])
        url = dict[scrape]
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')

        bold_tags = []
        for i in soup.find_all("span", class_="bold"):
            bold_tags.append(i.text)
        hr_tags = [i for i in bold_tags if i.startswith('HR')]
        print(len(hr_tags))
        print(hr_tags)

        df_list = pd.read_html(html, header=0)
        for c, table in enumerate(df_list):
            df = table
            df.iloc[:, 0].fillna(method='ffill', inplace=True)
            try:
                df.iloc[:, 1].fillna(method='ffill', inplace=True)
            except:
                'IndexError: single positional indexer is out-of-bounds'
            first_word = df.columns[0].split()[0]
            name = '\\{0}_{1}_{2}'.format(scrape, c, first_word)
            data_dir_name = data_dir + name
            df.to_excel(data_dir_name + ".xlsx", header=True, index=False)
            print(name + " exported!")
# def SDF_scrape
# def dropbox_scrape

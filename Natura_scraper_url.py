import os
import re

import numpy as np
import pandas as pd
import requests
from Natura_config import *
from bs4 import BeautifulSoup


# scraping from simple html urls
def law_scrape(scraping_list: list):
    # iterating over pages in list
    for count, scrape in enumerate(scraping_list):
        print(scrape, dict[scrape])
        url = dict[scrape]
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')

        bold_tags = []
        for i in soup.find_all("span", class_="bold"):
            bold_tags.append(i.text)
        if scrape == "POVS_PravilnikNN11122":
            hr_tags = [i for i in bold_tags if i.startswith('HR')]
            how_many_tables = []
            tables_counter = 0
            for c, i in enumerate(bold_tags):
                if i.startswith('HR'):
                    if tables_counter > 0:
                        how_many_tables.append(tables_counter)
                        tables_counter = 0
                    else:
                        tables_counter = 0
                if 'Cilj' in i:
                    tables_counter = tables_counter + 1
                if c == len(bold_tags) - 1:
                    how_many_tables.append(tables_counter)
            how_many_tables = np.cumsum(how_many_tables)

        # iterating over tables in list
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

            # special condition for tables scraped from this page
            if scrape == "POVS_PravilnikNN11122":
                first_word = "".join(ch for ch in first_word if ch.isalnum())
                second_word = first_word
                idx = 0
                for k in how_many_tables:
                    if c > k:
                        idx = idx + 1
                first_word = hr_tags[idx]
                if second_word == "Unnamed":
                    second_word = df.columns[1].split()[0]
                name = '\\{0}_{1}_{2}_{3}_{4}'.format(scrape, c, first_word, idx, second_word)

            data_dir_name = data_dir + name
            df.to_excel(data_dir_name + ".xlsx", header=True, index=False)
            print(name + " exported!")

def get_url_from_natura_links(sitecode, sitename):
    df = pd.read_excel(Natura_links)
    row = df.loc[(df['sitename'] == sitename) & (df['sitecode'] == sitecode)]
    url = row['url'].values[0]

def sdf_scrape(sitecode):
    assert isinstance(sitecode, str)
    url = 'https://natura2000.eea.europa.eu/Natura2000/SDF.aspx?site='+sitecode
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    df_list = pd.read_html(html, header=0)

    empty_table = []
    for c, table in enumerate(df_list):
        df = table
        first_word = df.columns[0].split()[0]
        if first_word == "Habitat":
            habitat = df
        if len(df)==0 and len(df.columns)==1 and c>10:
            empty_table.append(df)
            print(df)


# def dropbox_scrape

import os
import pandas as pd
import requests

from Natura_config import *

to_scrape: list[str] = ["Uredba_NN8019", "POP_PravilnikNN2520", "POP_PravilnikNN2520_ispravak"]


# scraping from simple html urls
def law_scrape(scraping_list: list):
    for count, scrape in enumerate(scraping_list):
        print(scrape, count, dict[scrape])
        url = dict[scrape]
        html = requests.get(url).content
        df_list = pd.read_html(html)
        df = df_list[0]

        name = '\\' + scrape + f'.xlsx'
        data_dir = f'{os.getcwd()}\\data'
        data_dir_name = data_dir + name
        df.to_excel(data_dir_name, header=False, index=False)


law_scrape(to_scrape)

import os
import pandas as pd


def find_roi(roi):
    data_dir = f'{os.getcwd()}\\data'
    data_list = os.listdir(data_dir)
    data_list = [s for s in data_list if "Identifikacijski.xlsx" in s]
    print(data_list)

    for c, i in enumerate(data_list):
        file = data_dir + "\\" + i
        df = pd.read_excel(file, header=0)
        # check if df contains ciljevi očuvanja, choose ciljevi očuvanja over other tables, if not then popis vrsta
        if df.loc[:,'Naziv područja'].str.contains(roi).any():
            df = df.loc[df['Naziv područja'] == roi]
            name = "\\{0}_{1}.xlsx".format(roi, c)
            data_dir_name = data_dir + name
            df.to_excel(data_dir_name)
            print(name + ' exported!')
        else:
            continue

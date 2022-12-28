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
        # classify the file by content
        if '0_Identifikacijski.xlsx' in i:
            EM = 'POP'
        if '3_Identifikacijski.xlsx' in i:
            EM = 'POP'
        if '4_Identifikacijski.xlsx' in i:
            EM = 'POVS'
        if '7_Identifikacijski.xlsx' in i:
            EM = 'JU'
        # filter roi in table, if it exists
        if df.loc[:, 'Naziv područja'].str.contains(roi).any():
            wanted_cols = [col for col in df.columns if 'Cilj' in col]
            df = df.loc[df['Naziv područja'] == roi]
            name = "\\{0}_{1}.xlsx".format(roi, c)
            data_dir_name = data_dir + name
            # formating the wanted POP table
            if EM == 'POP':
                df = df.fillna("")
                if len(wanted_cols) > 0:
                    df['Status vrste G-gnjezdarica, P-preletnica, Z-zimovalica'] = df.iloc[:, 5] + df.iloc[:,6] + df.iloc[:, 7]
                    df = df.drop(columns=['Kategorija za ciljnu vrstu', 'Mjere očuvanja', 'Status vrste  G-gnjezdarica',
                                          'Status vrste  P-preletnica', 'Status vrste  Z-zimovalica'])
                if len(wanted_cols) == 0:
                    df['Status vrste G-gnjezdarica, P-preletnica, Z-zimovalica'] = df.iloc[:,5] + df.iloc[:,6] + df.iloc[:,7]
                    df = df.drop(
                        columns=['Kategorija za ciljnu vrstu',
                                 'Status (G = gnjezdarica; P = preletnica;  Z = zimovalica)',
                                 'Status (G = gnjezdarica; P = preletnica;  Z = zimovalica).1',
                                 'Status (G = gnjezdarica; P = preletnica;  Z = zimovalica).2'])
            # formating the wanted POVS table
            if len(wanted_cols) == 0 and EM == 'POVS':
                df = df.drop(columns=['Kategorija za ciljnu vrstu/stanišni tip'])
            df.to_excel(data_dir_name, index=False)
            print(name + ' exported!')
            if len(wanted_cols) > 0:
                print("contains Ciljevi očuvanja")
            else:
                continue
        else:
            print("The Natura2000 region of interest was not found")

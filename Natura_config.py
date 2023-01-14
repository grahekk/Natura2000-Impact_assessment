import os

data_dir = f'{os.getcwd()}\\data'

dict = {"Uredba_NN8019": 'https://narodne-novine.nn.hr/clanci/sluzbeni/2019_08_80_1669.html',
        "Ciljeviocuvanja": 'https://www.dropbox.com/sh/3r4ozk30a21xzdz/AAA-B6wix9w8PgkdOo6Usu5ha/Ciljevi_ocuvanja_08112022.xlsx?dl=0',
        "Doradjeniciljevi": 'https://www.dropbox.com/sh/3r4ozk30a21xzdz/AAChIZ7H-JN3g4Z-kD2WowMDa/Doradjeni_ciljevi_ocuvanja?dl=0&subfolder_nav_tracking=1',
        "POP_PravilnikNN2520_ispravak": 'https://narodne-novine.nn.hr/clanci/sluzbeni/full/2020_03_38_822.html',
        "POVS_PravilnikNN11122": 'https://narodne-novine.nn.hr/clanci/sluzbeni/2022_09_111_1632.html'}

to_scrape: list[str] = ["Uredba_NN8019", "POP_PravilnikNN2520_ispravak", "POVS_PravilnikNN11122"]
template_name = "Template.docx"
Natura_links = data_dir + "\\Natura_links.xlsx"

import os
import pandoc
import pypandoc
import mammoth
from docx import Document
from bs4 import BeautifulSoup
from htmldocx import HtmlToDocx
from Natura_config import data_dir


def convert_template(file, format):
    file = data_dir + "\\" + file
    if format == 'md':
        with open(file, "rb") as docx_file:
            result = mammoth.convert_to_markdown(docx_file)
    if format == 'html':
        with open(file, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
    file = file.replace('docx','')
    with open(file + format, "w", encoding="utf-8") as new_file:
        new_file.write(result.value)


def create_report(template):
    filename = data_dir + "\\" + template
    new_file = data_dir + "\\New_document.html"
    table = data_dir + "\\Donja Posavina_0.xlsx.html"
    orig = 'Table_1'
    with open(table, 'r') as f:
        new = f.readlines()
    with open(filename, 'r') as f:
        text = f.readlines()
    # new_file = open(new_file, 'w')
    for line in text:
        new_text = line.replace(orig, ''.join(new))
        # print(new_text)
    # new_text = "\n".join([line if line != orig else new for line in text])
    # print(new_text)
    with open(new_file, 'w') as f:
        f.write(new_text)
        print("wrote")
        print(new_file)

def report_knit(template_file):
    filename = data_dir + "\\" + template_file
    new_parser = HtmlToDocx()
    #soup = BeautifulSoup(open(filename,'r'), "html.parser", from_encoding='UTF-8')
    #print(soup)
    new_parser.parse_html_file(filename, "New_document")
    #docx = new_parser.parse_html_string(filename)


# coding: utf-8
"""Utils functions used in knoema spider.
"""

from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
import json, os


def get_resource_path(path):
    dir_path = os.path.dirname(__file__)
    dir_path = dir_path if dir_path else os.getcwd()
    return os.path.join(dir_path, path)

# List of countries
with open(get_resource_path('./source_data/countries.json'), 'r', encoding='utf-8') as f:
    countries = [json.loads(line[:-1]) for line in f.readlines()]

# List of indicators
with open(get_resource_path('./source_data/indicators.json'), 'r', encoding='utf-8') as f:
    indicators = [json.loads(line[:-1]) for line in f.readlines()]


def load_table(html_soup):
    """Load table from html to list-dict format.
    """
    thead, tbody = html_soup.find('thead'), html_soup.find('tbody')
    keys = [th.text.replace('\xa0', ' ') for th in thead.find_all('th')]
    list_dict = []
    for tr in tbody.find_all('tr'):
        val_item = {}
        tds = tr.find_all('td')
        for i, key in enumerate(keys):
            val_item[key] = tds[i].text
        list_dict.append(val_item)
    return list_dict

def parse_num(str):
    """parse from str to float number.
    
    ie. '12.34 %' --> 0.1234
    ie. '123,456.789' --> 123456.789
    ie. '' --> 0
    ie. '12.34' --> 12.34
    """
    if "%" in str:
        return float(''.join(str.split('%'))) / 100.
    elif ',' in str:
        return float(''.join(str.split(',')))
    elif str == '':
        return 0
    else:
        return float(str)

def dropc(str, args):
    """drop args from str

    ie. dropc('abc\t\n\r', ['\t','\n','\r']) --> 'abc'
    """
    if args:
        return dropc(''.join(str.split(args[-1])), args[:-1])
    return str

def get_id_by_country(count_name):
    for count in countries:
        if count['name'] == count_name:
            return count['id']

def get_id_by_indic(indic_name):
    for indic in indicators:
        if indic['name'] == indic_name:
            return indic['id']

def load_data_file_to_dataframe(fpath):
    """load data file (json) to pd.DataFrame.
    """
    with open(fpath, 'r', encoding='utf-8') as f:
        data = [json.loads(line[:-1]) for line in f.readlines()]
    return pd.DataFrame(data)

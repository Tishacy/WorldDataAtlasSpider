# coding: utf-8
"""Spider of "www.knoema.com"
"""

import requests, re, os, json
from bs4 import BeautifulSoup
from qspider.core import QSpider, Task

from .utils import *


BASE_URL = "https://knoema.com/atlas/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Cookie': '_ga=GA1.2.1820746033.1545711260; __zlcmid=q2htJIu4k6vOpF; current-lang=en-US; KnoemaUserId=687bc257-09fd-4adf-8fd7-48f0338db287; _gid=GA1.2.350050298.1562062257; _fbp=fb.1.1562062265274.8020813; amplitude_id_4610ad0cc4acae5ee337e32b49325cdbknoema.com=eyJkZXZpY2VJZCI6ImY2YWQ3MDNiLTU3OTItNDUxNC1hZjI2LWMxNTRjMTA5MzVlNVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU2MjA2MjI1NzIzOCwibGFzdEV2ZW50VGltZSI6MTU2MjA2MjM1Njk4NywiZXZlbnRJZCI6MjYsImlkZW50aWZ5SWQiOjIsInNlcXVlbmNlTnVtYmVyIjoyOH0=; AWSALB=wZk3Obm8lhLHDTFXIfFeABHSPbsRoFpzpw1y5BssnhS3VUUSNcMApez3AkGE2w6YgRxXWpo1S0FqDtgY/GxGxNn0Mu5a6Dvr4cRLwv9fZjeoe0z6EWjj5nBQrGJx'}
SESS = requests.Session()
SESS.headers.update(HEADERS)


class Country(object):
    def __init__(self, country_name):
        self.country_name = country_name
        self.ini_country()
    
    def ini_country(self):
        target_url = "{0}/{1}".format(BASE_URL, self.country_name)
        html = SESS.get(target_url).text
        soup = BeautifulSoup(html, 'lxml')

        fact_div = soup.find('div', {'class': 'facts'})
        self.info = {}
        for li in fact_div.find_all('li'):
            if li.find_all('span'):
                # print(li.text)
                key, val = li.text.split(':')[0], ':'.join(li.text.split(':')[1:])
                redunc = ['\n','\t','\r']
                self.info[dropc(key, redunc)] = dropc(val, redunc)
    
    def fetch_data(self, indicator_name, mod=1):
        """fetch time series data of given indicator.

        params:
            indicator_name: (str) name of indicator
            mod: (int) 0/1
                0: fetch data by parsing html.
                1: fetch json data by post requests.
        return:
            (list dict) 
            ie. [{'time': '2000', 'val': 100}, {'time': '2001', 'val': 101}]
        """
        target_url = "{0}/{1}/{2}".format(BASE_URL, self.country_name, indicator_name)
        html = SESS.get(target_url).text
        soup = BeautifulSoup(html, 'lxml')

        if mod == 0:
            table = soup.find('table', {'class': 'knoema-table'})
            if not table:
                # 没有该指标数据
                return []
            data = load_table(table)
            unit = soup.find('span', {'class': 'italic'}).text[1:-1]
            for val_item in data:
                val_item['Indicator'] = indicator_name
                val_item['Unit'] = unit
                val_item['Value'] = parse_num(val_item['Value'])

        elif mod == 1:
            payload_data_tag = soup.find('input', {'name': 'datadescriptor'})
            if not payload_data_tag:
                # 没有该指标数据
                return []
            payload_data = payload_data_tag.attrs['value']
            payload_headers = {'Content-Type': 'application/json'}
            client_id = soup.find('input', {'id': 'systemClientId'}).attrs['value']    
            post_url = "https://knoema.com/api/1.0/data/pivot?reportErrorType=true&client_id=%s" %(client_id)
            res = SESS.post(post_url, data=payload_data, headers=payload_headers)
            res_data = json.loads(res.text)['data']
            data = []
            for data_item in res_data:
                item = {}
                item['Indicator'] = indicator_name
                item['Time'] = data_item['Time']
                item['Value'] = data_item['Value']
                item['Unit'] = data_item['Unit']
                item['RegionId'] = data_item['RegionId']
                item['country'] = data_item['country']
                data.append(item)

        return data
    
    def query(self, indicator_name, year):
        """query indicator by specific time (year).
        
        params:
            indicator_name: (str) name of indicator
            year: (str/int) specific year
        return:
            (list dict) ie. [{'time': '2000', 'val': 100}]
        """
        target_url = "{0}/{1}/{2}".format(BASE_URL, self.country_name, indicator_name)
        html = SESS.get(target_url).text
        soup = BeautifulSoup(html, 'lxml')

        payload_data = json.loads(soup.find('input', {'name': 'datadescriptor'}).attrs['value'])
        payload_data['Header'][0]['Members'] = [str(year)]

        payload_headers = {'Content-Type': 'application/json'}
        client_id = soup.find('input', {'id': 'systemClientId'}).attrs['value']
        post_url = "https://knoema.com/api/1.0/data/pivot?reportErrorType=true&client_id=%s" %(client_id)
        res = SESS.post(post_url, data=json.dumps(payload_data), headers=payload_headers)
        data = json.loads(res.text)['data']
        return data


def fetch_indicator_of_all_countries(indicator_name, out_path=''):
    """多线程爬虫爬取所有国家/地区的某指标数据
    """
    class QTask(Task):
        def __init__(self, task_source):
            Task.__init__(self, task_source)
            self.country = task_source
        
        def run(self):
            data = Country(self.country['name']).fetch_data(indicator_name)
            for item in data:
                content = json.dumps(item, ensure_ascii=False) + '\n'
                file.write(content)
                file.flush()
    if not out_path:
        out_path = './%s_of_all_countries.json' %(indicator_name)
    
    file = open(out_path, 'w', encoding='utf-8')
    # QSpider(countries, QTask).test()
    QSpider(countries, QTask, add_failed=False).crawl()


def fetch_all_indicators_of_country(country_name, out_path=''):
    """多线程爬虫爬取某国家/地区的所有指标数据
    """    
    class QTask(Task):
        def __init__(self, task_source):
            Task.__init__(self, task_source)
            self.indicator = task_source
        
        def run(self):
            data = country.fetch_data(self.indicator['name'])
            for item in data:
                content = json.dumps(item, ensure_ascii=False) + '\n'
                file.write(content)
                file.flush()
    
    country = Country(country_name)
    if not out_path:
        out_path = './all_indicators_of_%s.json' %(country_name)
    
    file = open(out_path, 'w', encoding='utf-8')
    # QSpider(indicators, QTask).test()
    QSpider(indicators, QTask, add_failed=False).crawl()


if __name__=="__main__":
    count = countries[115]['name']
    indic = indicators[12]['name']
    print(count, indic)
    CN = Country(count)

    # 查询
    pprint(CN.fetch_data(indic, mod=0))
    pprint(CN.query(indic, 2000))

    # 多线程爬取数据
    fetch_indicator_of_all_countries('GDP')
    fetch_all_indicators_of_country('China')
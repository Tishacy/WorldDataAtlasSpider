# coding: utf-8
"""Spider of "www.knoema.com"
"""

import requests, re, os, json
from bs4 import BeautifulSoup

from utils import *

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
        
        self.client_id = soup.find('input', {'id': 'systemClientId'}).attrs['value']
        self.payload_data = {"Dataset":"IMFWEO2019APR","Header":[{"FilterText":"null","DimensionId":"Time","Members":["1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"]}],"Stub":[{"FilterText":"null","DimensionId":"subject","Members":["1000010"]},{"FilterText": "null","DimensionId":"country","Members":["1001850"]}],"Filter":[],"Frequencies":["A"],"RegionIdsRequired":"false","RegionDimensionId":"null"}
        self.payload_headers = {'Content-Type': 'application/json'}

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
        if mod == 0:
            target_url = "{0}/{1}/{2}".format(BASE_URL, self.country_name, indicator_name)
            html = SESS.get(target_url).text
            soup = BeautifulSoup(html, 'lxml')

            table = soup.find('table', {'class': 'knoema-table'})
            data = load_table(table)
            unit = soup.find('span', {'class': 'italic'}).text[1:-1]
            for val_item in data:
                val_item['unit'] = unit
                val_item['Value'] = parse_num(val_item['Value'])

        elif mod == 1:
            post_url = "https://knoema.com/api/1.0/data/pivot?reportErrorType=true&client_id=%s" %(self.client_id)
            res = SESS.post(post_url, data=json.dumps(self.payload_data), headers=self.payload_headers)
            data = json.loads(res.text)['data']

        return data
    
    def query(self, indicator_name, year):
        """query indicator by specific time (year).
        
        params:
            indicator_name: (str) name of indicator
            year: (str/int) specific year
        return:
            (dict) ie. {'time': '2000', 'val': 100}
        """
        self.payload_data['Header'][0]['Members'] = [str(year)]
        post_url = "https://knoema.com/api/1.0/data/pivot?reportErrorType=true&client_id=%s" %(self.client_id)
        res = SESS.post(post_url, data=json.dumps(self.payload_data), headers=self.payload_headers)
        data_dict = json.loads(res.text)['data'][0]
        return data_dict


if __name__=="__main__":
    count = countries[15]
    indic = indicators[15]
    print(count, indic)
    CN = Country('China')
    pprint(CN.fetch_data(indic))
    pprint(CN.query(indic, 2003))

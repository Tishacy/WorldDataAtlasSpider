# -*- coding: utf-8 -*-

import requests, json
from bs4 import BeautifulSoup
from mspider.spider import MSpider

class Get_count_idSpider(MSpider):
    def __init__(self):
        self.name = "get_count_id"
        self.countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia-and-Herzegovina', 'Botswana', 'Brazil', 'Brunei-Darussalam', 'Bulgaria', 'Burkina-Faso', 'Burundi', 'Cabo-Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central-African-Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa-Rica', 'C%c3%b4te-dIvoire', 'Croatia', 'Cuba', 'Cyprus', 'Czech-Republic', 'Democratic-Peoples-Republic-of-Korea', 'Democratic-Republic-of-the-Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican-Republic', 'Ecuador', 'Egypt', 'El-Salvador', 'Equatorial-Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland-Islands', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong-Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Lao-Peoples-Democratic-Republic', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall-Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia-Federated-States-of', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New-Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua-New-Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Republic-of-Korea', 'Republic-of-Moldova', 'Romania', 'Russian-Federation', 'Rwanda', 'Saint-Kitts-and-Nevis', 'Saint-Lucia', 'Saint-Vincent-and-the-Grenadines', 'Samoa', 'San-Marino', 'Sao-Tome-and-Principe', 'Saudi-Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra-Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon-Islands', 'Somalia', 'South-Africa', 'South-Sudan', 'Spain', 'Sri-Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian-Arab-Republic', 'Taiwan-Province-of-China', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad-and-Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United-Arab-Emirates', 'United-Kingdom', 'United-Republic-of-Tanzania', 'United-States-of-America', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela-Bolivarian-Republic-of', 'Viet-Nam', 'Yemen', 'Zambia', 'Zimbabwe']
        self.urls = ['https://knoema.com/atlas/%s/Population' %(count) for count in self.countries]
        self.source = list(zip(self.countries, self.urls))
        self.file = open('./countries.json', 'w', encoding='utf-8')
        super(Get_count_idSpider, self).__init__(self.basic_func, self.source)

    def basic_func(self, index, src_item):
        count_name, url = src_item
        html = self.sess.get(url).text
        soup = BeautifulSoup(html, 'lxml')

        payload_data = json.loads(soup.find('input', {'name': 'datadescriptor'}).attrs['value'])
        item = {}
        item['id'] = str(payload_data['Stub'][1]['Members'][0])
        item['name'] = count_name
        # print(item)
        self.save_item(item)
    
    def save_item(self, item):
        content = json.dumps(item, ensure_ascii=False) + '\n'
        self.file.write(content)


if __name__=="__main__":
    spider = Get_count_idSpider()
    # spider.test()
    spider.crawl()
    spider.file.close()
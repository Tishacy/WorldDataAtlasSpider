# -*- coding: utf-8 -*-

import requests, json
from bs4 import BeautifulSoup
from mspider.spider import MSpider

class Get_indic_idSpider(MSpider):
    def __init__(self):
        self.name = "get_count_id"
        self.indics = ['GDP', 'GDP-based-on-PPP', 'Real-GDP-growth', 'GDP-per-capita', 'GDP-per-capita-based-on-PPP', 'Inflation-rate', 'Unemployment-rate', 'Current-account-balance', 'Current-account-balance-as-a-share-of-GDP', 'Government-gross-debt-as-a-share-of-GDP', 'Poverty-rate', 'International-reserves', 'Primary-energy-production', 'Primary-energy-consumption', 'Energy-intensity', 'Energy-imports', 'Alternative-and-nuclear-energy-use', 'Fossil-fuel-energy-consumption', 'Diesel-price', 'Gasoline-price', 'Air-transport-freight', 'Number-of-air-passengers-carried', 'Volume-of-goods-transported-by-railways', 'Number-of-passengers-carried-by-railways', 'Length-of-rail-lines', 'Road-density', 'Share-of-the-Internet-users', 'Share-of-households-with-Internet', 'Number-of-mobile-cellular-subscriptions', 'Military-expenditure', 'Military-expenditure-as-a-share-of-GDP', 'Arms-exports', 'Arms-imports', 'Exports', 'Goods-exports', 'Service-exports', 'Merchandise-exports', 'Food-exports', 'Fuel-exports', 'High-technology-exports', 'High-technology-exports-as-a-share-of-exports', 'Imports', 'Goods-imports', 'Service-imports', 'Merchandise-imports', 'Food-imports', 'Fuel-imports', 'Number-of-arrivals', 'Number-of-departures', 'Tourism-expenditures', 'Tourism-expenditures-as-a-share-of-imports', 'Expenditures-for-passenger-transport-items', 'Expenditures-for-travel-items', 'Tourism-receipts', 'Tourism-receipts-as-a-share-of-exports', 'Receipts-for-passenger-transport-items', 'Receipts-for-travel-items', 'CO2-emissions', 'CO2-emissions-per-capita', 'CO2-emissions-intensity', 'Quantity-of-municipal-waste-collected', 'Human-development-index', 'Ease-of-doing-business-index', 'Global-competitiveness-index', 'Corruption-perceptions-index', 'Index-of-economic-freedom', 'Press-freedom-index', 'Political-rights-index', 'Civil-liberties-index', 'Property-rights-index', 'Prosperity-index', 'Happiness', 'Population', 'Population-growth-rate', 'Population-density', 'Urban-population', 'Birth-rate', 'Death-rate', 'Fertility-rate', 'Population-aged-0-14-years', 'Population-aged-15-64-years', 'Population-aged-65-years-and-above', 'Female-population', 'Employment-to-population-ratio', 'Land-area', 'Agricultural-land-area', 'Agricultural-land-as-a-share-of-land-area', 'Forest-area-as-a-share-of-land-area', 'Agriculture-value-added-per-worker', 'Food-production-index', 'Livestock-production-index', 'Crop-production-index', 'Cereal-production', 'Cereal-yield', 'Land-under-cereal-production', 'Number-of-tractors', 'Fertilizer-consumption', 'Neonatal-mortality-rate', 'Infant-mortality-rate', 'Child-mortality-rate', 'Maternal-mortality-ratio', 'Life-expectancy', 'Health-expenditure-as-a-share-of-GDP', 'Health-expenditure-per-capita', 'HIV-prevalence', 'Incidence-of-tuberculosis', 'Female-obesity-prevalence', 'Male-obesity-prevalence', 'Education-expenditure', 'Primary-enrollment', 'Duration-of-primary-education', 'Duration-of-secondary-education', 'Pupil-teacher-ratio-in-primary-education', 'Pupil-teacher-ratio-in-secondary-education', 'Adult-literacy-rate', 'Youth-literacy-rate', 'Homicide-rate', 'Number-of-homicides', 'Number-of-homicides-by-firearm', 'Share-of-homicides-by-firearm', 'Homicides-by-firearm-rate', 'Assault-rate', 'Kidnapping-rate', 'Robbery-rate', 'Rape-rate', 'Burglary-rate', 'Private-car-theft-rate', 'Motor-vehicle-theft-rate', 'Burglary-and-housebreaking-rate', 'Poverty-rate-at-dollar19-a-day', 'Poverty-rate-at-dollar32-a-day', 'Poverty-rate-at-national-poverty-line', 'Rural-poverty-rate', 'Urban-poverty-rate', 'GINI-index', 'Income-share-held-by-lowest-10percent', 'Income-share-held-by-highest-10percent', 'Prevalence-of-undernourishment', 'Number-of-undernourished-people', 'Food-deficit', 'Dietary-energy-supply-adequacy', 'Precipitation', 'Precipitation-volume', 'Rainfall-index', 'Volume-of-groundwater-produced', 'Volume-of-surface-water-produced', 'Internal-renewable-water-resources-per-capita', 'Renewable-water-resources-per-capita', 'Dependency-ratio', 'Freshwater-withdrawals', 'Water-productivity', 'RandD-expenditure', 'Number-of-researchers-in-RandD', 'Number-of-technicians-in-RandD', 'Number-of-scientific-journal-articles', 'Number-of-patent-applications']
        self.urls = ['https://knoema.com/atlas/United-States-of-America/%s' %(indic) for indic in self.indics]
        self.source = list(zip(self.indics, self.urls))
        self.file = open('./indicators.json', 'w', encoding='utf-8')
        super(Get_indic_idSpider, self).__init__(self.basic_func, self.source)

    def basic_func(self, index, src_item):
        indic, url = src_item
        html = self.sess.get(url).text
        soup = BeautifulSoup(html, 'lxml')

        payload_data = json.loads(soup.find('input', {'name': 'datadescriptor'}).attrs['value'])
        item = {}
        item['id'] = str(payload_data['Stub'][0]['Members'][0])
        item['name'] = indic
        # print(item)
        self.save_item(item)
    
    def save_item(self, item):
        content = json.dumps(item, ensure_ascii=False) + '\n'
        self.file.write(content)
        self.file.flush()

if __name__=="__main__":
    spider = Get_indic_idSpider()
    # spider.test()
    spider.crawl()
    spider.file.close()
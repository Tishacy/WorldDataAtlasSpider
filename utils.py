# coding: utf-8
"""Utils functions used in knoema spider.
"""

from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd

# List of countries
countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia-and-Herzegovina', 'Botswana', 'Brazil', 'Brunei-Darussalam', 'Bulgaria', 'Burkina-Faso', 'Burundi', 'Cabo-Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central-African-Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa-Rica', 'C%c3%b4te-dIvoire', 'Croatia', 'Cuba', 'Cyprus', 'Czech-Republic', 'Democratic-Peoples-Republic-of-Korea', 'Democratic-Republic-of-the-Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican-Republic', 'Ecuador', 'Egypt', 'El-Salvador', 'Equatorial-Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland-Islands', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong-Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Lao-Peoples-Democratic-Republic', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall-Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia-Federated-States-of', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New-Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua-New-Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Republic-of-Korea', 'Republic-of-Moldova', 'Romania', 'Russian-Federation', 'Rwanda', 'Saint-Kitts-and-Nevis', 'Saint-Lucia', 'Saint-Vincent-and-the-Grenadines', 'Samoa', 'San-Marino', 'Sao-Tome-and-Principe', 'Saudi-Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra-Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon-Islands', 'Somalia', 'South-Africa', 'South-Sudan', 'Spain', 'Sri-Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian-Arab-Republic', 'Taiwan-Province-of-China', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad-and-Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United-Arab-Emirates', 'United-Kingdom', 'United-Republic-of-Tanzania', 'United-States-of-America', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela-Bolivarian-Republic-of', 'Viet-Nam', 'Yemen', 'Zambia', 'Zimbabwe']

# List of indicators
indicators = ['GDP', 'GDP-based-on-PPP', 'Real-GDP-growth', 'GDP-per-capita', 'GDP-per-capita-based-on-PPP', 'Inflation-rate', 'Unemployment-rate', 'Current-account-balance', 'Current-account-balance-as-a-share-of-GDP', 'Government-gross-debt-as-a-share-of-GDP', 'Poverty-rate', 'International-reserves', 'Primary-energy-production', 'Primary-energy-consumption', 'Energy-intensity', 'Energy-imports', 'Alternative-and-nuclear-energy-use', 'Fossil-fuel-energy-consumption', 'Diesel-price', 'Gasoline-price', 'Air-transport-freight', 'Number-of-air-passengers-carried', 'Volume-of-goods-transported-by-railways', 'Number-of-passengers-carried-by-railways', 'Length-of-rail-lines', 'Road-density', 'Share-of-the-Internet-users', 'Share-of-households-with-Internet', 'Number-of-mobile-cellular-subscriptions', 'Military-expenditure', 'Military-expenditure-as-a-share-of-GDP', 'Arms-exports', 'Arms-imports', 'Exports', 'Goods-exports', 'Service-exports', 'Merchandise-exports', 'Food-exports', 'Fuel-exports', 'High-technology-exports', 'High-technology-exports-as-a-share-of-exports', 'Imports', 'Goods-imports', 'Service-imports', 'Merchandise-imports', 'Food-imports', 'Fuel-imports', 'Number-of-arrivals', 'Number-of-departures', 'Tourism-expenditures', 'Tourism-expenditures-as-a-share-of-imports', 'Expenditures-for-passenger-transport-items', 'Expenditures-for-travel-items', 'Tourism-receipts', 'Tourism-receipts-as-a-share-of-exports', 'Receipts-for-passenger-transport-items', 'Receipts-for-travel-items', 'CO2-emissions', 'CO2-emissions-per-capita', 'CO2-emissions-intensity', 'Quantity-of-municipal-waste-collected', 'Human-development-index', 'Ease-of-doing-business-index', 'Global-competitiveness-index', 'Corruption-perceptions-index', 'Index-of-economic-freedom', 'Press-freedom-index', 'Political-rights-index', 'Civil-liberties-index', 'Property-rights-index', 'Prosperity-index', 'Happiness', 'Population', 'Population-growth-rate', 'Population-density', 'Urban-population', 'Birth-rate', 'Death-rate', 'Fertility-rate', 'Population-aged-0-14-years', 'Population-aged-15-64-years', 'Population-aged-65-years-and-above', 'Female-population', 'Employment-to-population-ratio', 'Land-area', 'Agricultural-land-area', 'Agricultural-land-as-a-share-of-land-area', 'Forest-area-as-a-share-of-land-area', 'Agriculture-value-added-per-worker', 'Food-production-index', 'Livestock-production-index', 'Crop-production-index', 'Cereal-production', 'Cereal-yield', 'Land-under-cereal-production', 'Number-of-tractors', 'Fertilizer-consumption', 'Neonatal-mortality-rate', 'Infant-mortality-rate', 'Child-mortality-rate', 'Maternal-mortality-ratio', 'Life-expectancy', 'Health-expenditure-as-a-share-of-GDP', 'Health-expenditure-per-capita', 'HIV-prevalence', 'Incidence-of-tuberculosis', 'Female-obesity-prevalence', 'Male-obesity-prevalence', 'Education-expenditure', 'Primary-enrollment', 'Duration-of-primary-education', 'Duration-of-secondary-education', 'Pupil-teacher-ratio-in-primary-education', 'Pupil-teacher-ratio-in-secondary-education', 'Adult-literacy-rate', 'Youth-literacy-rate', 'Homicide-rate', 'Number-of-homicides', 'Number-of-homicides-by-firearm', 'Share-of-homicides-by-firearm', 'Homicides-by-firearm-rate', 'Assault-rate', 'Kidnapping-rate', 'Robbery-rate', 'Rape-rate', 'Burglary-rate', 'Private-car-theft-rate', 'Motor-vehicle-theft-rate', 'Burglary-and-housebreaking-rate', 'Poverty-rate-at-dollar19-a-day', 'Poverty-rate-at-dollar32-a-day', 'Poverty-rate-at-national-poverty-line', 'Rural-poverty-rate', 'Urban-poverty-rate', 'GINI-index', 'Income-share-held-by-lowest-10percent', 'Income-share-held-by-highest-10percent', 'Prevalence-of-undernourishment', 'Number-of-undernourished-people', 'Food-deficit', 'Dietary-energy-supply-adequacy', 'Precipitation', 'Precipitation-volume', 'Rainfall-index', 'Volume-of-groundwater-produced', 'Volume-of-surface-water-produced', 'Internal-renewable-water-resources-per-capita', 'Renewable-water-resources-per-capita', 'Dependency-ratio', 'Freshwater-withdrawals', 'Water-productivity', 'RandD-expenditure', 'Number-of-researchers-in-RandD', 'Number-of-technicians-in-RandD', 'Number-of-scientific-journal-articles', 'Number-of-patent-applications']

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

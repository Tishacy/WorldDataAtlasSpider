# coding: utf-8
"""Demo: Comparison of GDP between USA and China from 1980-2014
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from knoema import Country
from utils import *


# Fetch data
INDIC = 'Population'
CN, USA = Country('China'), Country('USA')
CN_data, USA_data = CN.fetch_data(INDIC), USA.fetch_data(INDIC)
CN_df, USA_df = pd.DataFrame(CN_data), pd.DataFrame(USA_data)
print('已获取数据')

# Visualization
fig = plt.figure(figsize=(8, 4.5))
frm = int(CN_data[0]['Time'][:4])

plt.plot(np.arange(frm, frm + len(CN_data)), 'Value', '-o', color='r', data=CN_df, label='CN')
plt.plot(np.arange(frm, frm + len(USA_data)), 'Value', '-o', color='k', data=USA_df, label='USA')
plt.xlabel('Time (a)', fontsize=14)
plt.ylabel('{0} ({1})'.format(INDIC, CN_data[0]['Unit']), fontsize=14)
plt.title('Comparison of %s between USA and CN' %(INDIC), fontsize=15)
plt.legend(fontsize=12)
fig.autofmt_xdate()

plt.show()

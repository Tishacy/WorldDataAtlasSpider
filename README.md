# World Data Atlas (Knoema) Spider

通过 [Knoema](https://knoema.com/atlas) 获取 **某国家/地区** 的 **某指标** 的 **不同年份** 的数据。

- 可获取数据的国家/地区见 [`./knoema/source_data/countries.json`](https://github.com/Tishacy/WorldDataAtlas/blob/master/knoema/source_data/countries.json)。
- 可获取数据的指标见[`./knoema/source_data/indicators.json`](https://github.com/Tishacy/WorldDataAtlas/blob/master/knoema/source_data/indicators.json)。

目录树如下：

```bash
.
├── demo.py                     # 简单的demo
├── demo.png
├── handbook.ipynb              # handbook (jupyter notebook)
├── knoema                      # 爬虫主目录
│   ├── __init__.py
│   ├── knoema.py               # 爬虫主文件
│   ├── source_data             # 爬虫源数据
│   │   ├── countries.json
│   │   ├── get_count_id.py
│   │   ├── get_indic_id.py
│   │   └── indicators.json
│   └── utils.py                # 爬虫工具函数模块
├── README.md
├── LICENSE
└── requirements.txt
```

## Pre-requirements

1. 克隆至本地。

    ```bash
    $ git clone https://github.com/Tishacy/WorldDataAtlas.git
    $ cd WorldDataAtlas
    ```

2. 依赖库如下：

    ```bash
    mspider==0.2.5
    numpy==1.13.3
    pandas==0.24.2
    requests==2.18.4
    matplotlib==3.0.1
    beautifulsoup4==4.7.1
    ```
    安装依赖：

    ```bash
    $ pip install -r requirements.txt
    ```

## Usage

### Quick start

获取美国的GDP数据。

1. 在仓库主目录下新建python文件或打开IPython console。

2. 导入`knoema`模块。

  ```python
  from knoema.knoema import Country
  from knoema.utils import *
  ```

3. 创建Country对象。

   ```python
   US = Country('USA')
   # 或者使用国家/地区全称
   # US = Country('United-States-of-America')
   ```

4. 获取美国往年GDP数据。

    ```python
    US.fetch_data('GDP')
    ```

    得到：

    ```json
    [{'Indicator': 'GDP',
      'Time': '1980-01-01T00:00:00Z',
      'Value': 2857.33,
      'Unit': 'U.S. dollars, Billions',
      'RegionId': 'US',
      'country': 'United States'},
     {'Indicator': 'GDP',
      'Time': '1981-01-01T00:00:00Z',
      'Value': 3207.03,
      'Unit': 'U.S. dollars, Billions',
      'RegionId': 'US',
      'country': 'United States'},
        ...
     {'Indicator': 'GDP',
      'Time': '2018-01-01T00:00:00Z',
      'Value': 20494.05,
      'Unit': 'U.S. dollars, Billions',
      'RegionId': 'US',
      'country': 'United States'}]
    ```

5. 获取2015年美国GDP数据。

   ```python
   US.query('GDP', '2015')
   ```

   得到：

   ```json
   [{'Time': '2015-01-01T00:00:00Z',
     'country': 'United States',
     'RegionId': 'US',
     'subject': 'Gross domestic product, current prices (U.S. dollars)',
     'Frequency': 'A',
     'Value': 18219.3,
     'Unit': 'U.S. dollars, Billions',
     'Scale': 1}]
   ```

### 运行demo

`demo.py`：获取中国和美国的GDP数据并绘制图像。

```bash
$ python3 demo.py
```

若见下图，则运行成功。

![Figure of demo](./demo.png)

### 具体用法

**见[`handbook.ipynb`](http://nbviewer.jupyter.org/github/Tishacy/WorldDataAtlas/blob/master/handbook.ipynb)。**



## License

Copyright (c) 2019 tishacy.

Licensed under the [MIT License](https://github.com/Tishacy/WorldDataAtlas/blob/master/LICENSE).
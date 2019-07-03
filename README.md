# Python spider of world data atlas

爬取获取 **某国家/地区** 的 **某指标** 的 **不同年份** 的数据。

```bash
.
├── demo.py						# 简单的demo
├── demo.png
├── handbook.ipynb				# handbook (jupyter notebook)
├── knoema						# 爬虫主目录
│   ├── __init__.py
│   ├── knoema.py				# 爬虫主文件
│   ├── source_data				# 爬虫源数据
│   │   ├── countries.json
│   │   ├── get_count_id.py
│   │   ├── get_indic_id.py
│   │   └── indicators.json
│   └── utils.py				# 爬虫工具函数模块
├── README.md
├── LICENSE
└── requirements.txt
```

## Pre-requirements

```bash
$ pip install -r requirements.txt
```

## Usage

### 运行demo

`demo.py`：获取中国和美国的人口数据并绘制图像。

```bash
$ python3 demo.py
```

![Figure of demo](./demo.png)

### 具体用法

见[`handbook.ipynb`](http://nbviewer.jupyter.org/github/Tishacy/WorldDataAtlas/blob/master/handbook.ipynb)。



## License

Copyright (c) 2019 tishacy.

Licensed under the [MIT License](https://github.com/Tishacy/WorldDataAtlas/blob/master/LICENSE).
import pandas as pd

data = pd.read_csv('lianjia_zufang.csv')

datas = data.drop_duplicates(['链接'])  # inplace = False

datas.to_csv('lianjia_zufang2.csv')

# 写入后多出了一列 'Unnamed: 0'

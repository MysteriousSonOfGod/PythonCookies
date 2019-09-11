import re

import matplotlib.pyplot as plt
import pandas as pd

datas = pd.read_csv('lianjia_zufang.csv')
datas = datas[['链接', '价格', '面积']]

datas.index = [url[7: 9] for url in datas['链接']]

datas.groupby([datas.index]).describe()
datas.ix['gz']['价格'].sum()
meanPrices = datas.groupby([datas.index]).mean()
fig = plt.figure(1)
plt.plot(meanPrices['价格'].values)
plt.xlim(0, 20)
plt.grid()
num = 0
for meanPrice in meanPrices.index:
    plt.annotate(meanPrice,
                 xy=(num, meanPrices['价格'].values[num]), xytext=(-20, 20), textcoords='offset points', ha='right',
                 va='bottom',
                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                 arrowprops=dict(arrowstyle='->', facecolor='black', connectionstyle='arc3,rad=0'))
    num += 1


# plt.show()


def areas(num):
    return re.search('(.*?)平米', num).group(1)


datas['areas'] = datas['面积'].apply(areas).astype(float)

datas.groupby([datas.index])['areas'].describe()

meanAreas = datas.groupby([datas.index])['areas'].mean()
fig = plt.figure(2)
plt.plot(meanAreas.values)
plt.xlim(0, 20)
plt.grid()
num = 0
for index in meanPrices.index:
    plt.annotate(index,
                 xy=(num, meanAreas[num]), xytext=(-20, 20), textcoords='offset points', ha='right', va='bottom',
                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                 arrowprops=dict(arrowstyle='->', facecolor='black', connectionstyle='arc3,rad=0'))
    num += 1

plt.show()

import csv

file = 'doubanbooks.csv'


def create_csv():
    fieldnames = ['书名', '作者', '豆瓣评分', '简介']
    with open(file, 'w', encoding='utf8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


create_csv()

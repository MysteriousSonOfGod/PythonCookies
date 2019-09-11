# coding=utf8

import csv
import io

import pandas as pd
from xlsxwriter import Workbook

players = [
    {'dailyWinners': 3, 'dailyFreePlayed': 2, 'user': 'Player1', 'bank': 0.06},
    {'dailyWinners': 3, 'dailyFreePlayed': 2, 'user': 'Player2', 'bank': 4.0},
    {'dailyWinners': 1, 'dailyFree': 2, 'user': 'Player3', 'bank': 3.1},
    {'dailyWinners': 3, 'dailyFree': 2, 'user': 'Player4', 'bank': 0.32}
]

INF = 'INF'

graph = {'A': {'A': 0, 'B': 6, 'C': INF, 'D': 6, 'E': 7},

         'B': {'A': INF, 'B': 0, 'C': 5, 'D': INF, 'E': INF},

         'C': {'A': INF, 'B': INF, 'C': 0, 'D': 9, 'E': 3},

         'D': {'A': INF, 'B': INF, 'C': 9, 'D': 0, 'E': 7},

         'E': {'A': INF, 'B': 4, 'C': INF, 'D': INF, 'E': 0}
         }


def dict2csv(datas):
    keys = {key for data in datas for key in data.keys()}
    output = io.StringIO()
    writer = csv.DictWriter(output, keys)
    writer.writeheader()
    writer.writerows(players)
    output.seek(0)
    return output


def dict2excel(dts):
    keys = list({key for data in dts for key in data.keys()})
    file_object = io.BytesIO()
    wb = Workbook(file_object)
    ws = wb.add_worksheet()
    first_row = 0
    for header in keys:
        col = keys.index(header)
        ws.write(first_row, col, header)

    row = 1
    for dt in dts:
        for _key, _value in dt.items():
            col = keys.index(_key)
            ws.write(row, col, _value)
        row += 1
    wb.close()
    file_object.seek(0)
    return file_object


def dict2excel2(datas):
    df = pd.DataFrame.from_dict(datas)
    df.to_excel('file.xlsx')


def dict2fl(graph):
    df = pd.DataFrame(graph).T
    df.to_csv('file.csv')
    df.to_excel('file.xlsx')


if __name__ == '__main__':
    pass

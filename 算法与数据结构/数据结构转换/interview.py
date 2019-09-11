# coding=utf8

import csv
from collections import defaultdict


def csv2json(file_path):
    def main_tree():
        return defaultdict(main_tree)

    def get_leaf(name, leaf):
        return {name: [get_leaf(k, v) for k, v in leaf.items()]}

    def add_tree(_tree, values):
        for val in values:
            _tree = _tree[val]

    tree = main_tree()
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        value = []
        for row_index, row_val in enumerate(reader):
            # 假设第一行有数值
            value.append([])
            if not row_val[0]:
                row_val[0] = value[row_index - 1][0]
            for each_index, each_val in enumerate(row_val):
                if not each_val:
                    each_val = value[row_index - 1][each_index]
                value[row_index].append(each_val)
            add_tree(tree, value[row_index])
        result = [get_leaf(root, leaf) for root, leaf in tree.items()]
        # in this case only one root
    return result[0]


def find(key):
    data = csv2json('history.csv')

    def search_parent(dt, val, key_path):
        if dt == val:
            return key_path
        if isinstance(dt, (dict,)):
            for _key, _val in dt.items():
                if _val == val:
                    result = search_parent(data, dt, _key + "." + key_path)
                    if result:
                        return result
                else:
                    result = search_parent(_val, val, key_path)
                    if result:
                        return result
        elif isinstance(dt, (list,)):
            for each_dt in dt:
                if each_dt == val:
                    result = search_parent(data, dt, key_path)
                    if result:
                        return result
                else:
                    result = search_parent(each_dt, val, key_path)
                    if result:
                        return result

    def search_val(search_data):
        if isinstance(search_data, (dict,)):
            for each_key, each_val in search_data.items():
                if each_key == key:
                    result = search_parent(data, search_data, key)
                    return result
                else:
                    result = search_val(each_val)
                    if result:
                        return result
        elif isinstance(search_data, (list,)):
            for each in search_data:
                result = search_val(each)
                if result:
                    return result

    output = search_val(data)
    if not output:
        output = '未找到关键字：{0}'.format(key)
    return output


if __name__ == '__main__':
    from pprint import pprint

    data = csv2json('history.csv')
    pprint(data)
    result0, result1 = find("汉谟拉比法典"), find('美洲')
    print(result0, result1)

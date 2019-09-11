import operator
import re
import string
from collections import defaultdict


def cleanInput(put):
    put = re.sub('[\n| ]+', ' ', put).lower()
    put_data = put.split(' ')
    clean_data = []
    for item in put_data:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item == 'a' or item == 'i'):
            clean_data.append(item)
    return clean_data


def ngrams(put, n):
    put = cleanInput(put)
    outPut = defaultdict(int)
    for i in range(len(put) - n + 1):
        ngramTemp = " ".join(put[i:i + n])
        outPut[ngramTemp] += 1
    return outPut


if __name__ == '__main__':
    with open('inaugurationSpeech.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    ngrams = ngrams(data, 2)
    sortedNGrams = sorted(ngrams.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedNGrams)

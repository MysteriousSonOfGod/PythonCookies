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
        if not isCommon(put[i: i + n]):
            ngramTemp = " ".join(put[i:i + n])
            outPut[ngramTemp] += 1
    return outPut


def isCommon(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it",
                   "i", "that", "for", "you", "he", "with", "on", "do", "say", "this",
                   "they", "is", "an", "at", "but", "we", "his", "from", "that", "not",
                   "by", "she", "or", "as", "what", "go", "their", "can", "who", "get",
                   "if", "would", "her", "all", "my", "make", "about", "know", "will",
                   "as", "up", "one", "time", "has", "been", "there", "year", "so",
                   "think", "when", "which", "them", "some", "me", "people", "take",
                   "out", "into", "just", "see", "him", "your", "come", "could", "now",
                   "than", "like", "other", "how", "then", "its", "our", "two", "more",
                   "these", "want", "way", "look", "first", "also", "new", "because",
                   "day", "more", "use", "no", "man", "find", "here", "thing", "give",
                   "many", "well"]
    for word in ngram:
        if word in commonWords:
            return True
    return False


if __name__ == '__main__':
    with open('inaugurationSpeech.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    ngrams = ngrams(data, 2)
    sortedNGrams = sorted(ngrams.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedNGrams)

import jieba
from matplotlib.pylab import (imshow, show)
from wordcloud import WordCloud


def ciyun(file):
    with open(file) as f:
        text = f.read()

    wordlist = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(wordlist)
    my_wordcloud = WordCloud().generate(wl_space_split)
    imshow(my_wordcloud)
    show()


if __name__ == '__main__':
    ciyun('views')

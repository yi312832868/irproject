# !/usr/bin/python
# encoding: UTF-8
import requests
from bs4 import BeautifulSoup
import re
import time
import os


# make English text clean
def clean_en_text(text):
    # keep English, digital and space
    comp = re.compile('[^A-Z^a-z^0-9^ ]')
    return comp.sub('', text)


def clean_zh_text(text):
    # keep English, digital and Chinese
    comp = re.compile('[^A-Z^a-z^0-9^ ^\u4e00-\u9fa5]')
    return comp.sub('', text)


mark = {"en": 1, "zh": 2}


def is_zh(c):
    x = ord(c)
    # Punct & Radicals
    if x >= 0x2e80 and x <= 0x33ff:
        return True

    # Fullwidth Latin Characters
    elif x >= 0xff00 and x <= 0xffef:
        return True

    # CJK Unified Ideographs &
    # CJK Unified Ideographs Extension A
    elif x >= 0x4e00 and x <= 0x9fbb:
        return True
    # CJK Compatibility Ideographs
    elif x >= 0xf900 and x <= 0xfad9:
        return True

    # CJK Unified Ideographs Extension B
    elif x >= 0x20000 and x <= 0x2a6d6:
        return True

    # CJK Compatibility Supplement
    elif x >= 0x2f800 and x <= 0x2fa1d:
        return True

    else:
        return False


def split_zh_en(zh_en_str):
    zh_en_group = []
    zh_gather = ""
    en_gather = ""
    zh_status = False

    for c in zh_en_str:
        if not zh_status and is_zh(c):
            zh_status = True
            if en_gather != "":
                zh_en_group.append([mark["en"], en_gather])
                en_gather = ""
        elif not is_zh(c) and zh_status:
            zh_status = False
            if zh_gather != "":
                zh_en_group.append([mark["zh"], zh_gather])
        if zh_status:
            zh_gather += c
        else:
            en_gather += c
            zh_gather = ""

    # if en_gather != "":
    zh_en_group.append([mark["en"], en_gather])
    # elif zh_gather != "":
    zh_en_group.append([mark["zh"], zh_gather])
    return zh_en_group


def sentence_split(str_centence):
    ###分词函数
    list_ret = list()
    str_centence = split_EN_ZH(str_centence)
    str_centence = str_centence.lower()
    list_ret = str_centence.split()
    return list_ret


def split_EN_ZH(keyPhrase):
    x = split_zh_en(keyPhrase)[0][1]
    y = split_zh_en(keyPhrase)[1][1]
    l = ""
    for zh_word in clean_zh_text(x):
        l = l + zh_word + " "
    for en_word in clean_en_text(keyPhrase).split():
        l = l + en_word + " "
    return l


def focusedCrawler(url, keyPhrase):
    time.sleep(1)
    # print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    head = str(soup.head)
    # <head> </head>     <title></title>
    head = head[6:-8]
    combine = head
    total = sentence_split(combine)
    allwords = {}  # all words in url
    query = {}  # all words query have
    tags = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
    for word in total:
        if word in tags:
            continue
        if word not in allwords:
            allwords[word] = 1
        else:
            allwords[word] += 1
    for word in sentence_split(keyPhrase):
        if word not in query:
            query[word] = 1
        else:
            query[word] += 1
    molecule = 0  # 分子
    A = 0
    B = 0
    for word in query:
        if word in allwords:
            molecule += query[word] * allwords[word]
        A += query[word] * query[word]
    for word in allwords:
        B += allwords[word] * allwords[word]
    Denominator = (A * B) ** 0.5  # 分母
    result = molecule / Denominator
    print("url:" + url + "\n cos:" + str(result))


#focusedCrawler(url='https://www.tesla.com/models', keyPhrase='特斯拉car performance')

f = open("url.txt", 'r')
lines = f.readlines()
lists = []
for line in lines:
    lists.append(line)

print(list)

for x in lists:
    y = x.split()
    focusedCrawler(y[0],keyPhrase='特斯拉car performance')
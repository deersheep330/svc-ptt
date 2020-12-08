from copy import deepcopy

from ptt.nlp import JiebaPipeline
from ptt.parser import PttParser
import socket
import requests

if __name__ == '__main__':

    # parse ptt articles
    parser = PttParser('Stock')
    articles = parser.get_articles()
    list_without_content = parser.get_sentence_list_without_content()
    list_title_only = parser.get_title_list()

    resp = requests.get('http://localhost:7777/stocks')
    arr = []
    for ele in resp.json():
        arr.append(ele['symbol'])
        arr.append(ele['name'])

    years = ['2020', '2021', '2022', '2023', '2024', '2025', 'DDD', 'VVV']

        # tokenization with jieba
    pipeline = JiebaPipeline()

    # count words for title + pushes
    pipeline.set_custom_dict(arr) \
        .tokenize(list_without_content) \
        .remove_words_from_token_list(years) \
        .keep_words_from_token_list(arr) \
        .count_tokens()
    title_and_pushes_freq = deepcopy(pipeline.token_freq)
    print(title_and_pushes_freq)

    # count words for title only
    pipeline.tokenize(list_title_only) \
        .remove_words_from_token_list(years) \
        .keep_words_from_token_list(arr) \
        .count_tokens()
    title_only_freq = deepcopy(pipeline.token_freq)

    # if an article's title contains a keyword,
    # add number of pushes of this article to this keyword
    title_only_freq = dict(title_only_freq)
    for key, value in title_only_freq.items():
        for article in parser.get_articles():
            if key in article.title:
                title_only_freq[key] += article.push_count

    # after addition, sort again
    title_only_freq = sorted(title_only_freq.items(), key=lambda x: x[1], reverse=True)
    print(title_only_freq)

'''
    resp = requests.get('http://localhost:7777/stocks')
    print(resp.json())
'''

'''
    print(socket.gethostbyname('localhost'))
    print(socket.gethostbyname('google.com'))
    print(socket.gethostbyname('db'))
'''

'''
    # parse ptt articles
    parser = PttParser('Stock')
    articles = parser.get_articles()
'''
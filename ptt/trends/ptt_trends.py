from copy import deepcopy

from ptt.nlp import JiebaPipeline
from ptt.parser import PttParser
import socket
import requests

def get_db_hostname():
    try:
        socket.gethostbyname('db')
        print(f'db hostname = db')
        return 'db'
    except Exception as e:
        print(f'gethostbyname(\'db\') failed: {e}')
        print(f'db hostname = localhost')
        return 'localhost'

class PttTrends():

    def __init__(self):

        # step 1
        # get stock symbols and names for constructing custom dict later
        resp = requests.get(f'http://{get_db_hostname()}:7777/stocks')
        #print(resp.json())
        self.custom_words = []
        for ele in resp.json():
            self.custom_words.append(ele['symbol'])
            self.custom_words.append(ele['name'])

        # step 2
        # for removing meaningless words later
        # prevent them from being treated as stock symbols
        self.excludes = ['2020', '2021', '2022', '2023', '2024', '2025', 'DDD', 'VVV']

        # step 3
        # parse ptt articles
        self.parser = PttParser('Stock')
        # article title + pushes
        self.sentence_list = self.parser.get_sentence_list_without_content()
        # article title only
        self.title_list = self.parser.get_title_list()

        # step 4
        # tokenization with jieba
        self.pipeline = JiebaPipeline()
        # calculate word freq for title + pushes
        self.pipeline \
            .set_custom_dict(self.custom_words) \
            .tokenize(self.sentence_list) \
            .remove_words_from_token_list(self.excludes) \
            .keep_words_from_token_list(self.custom_words) \
            .count_tokens()
        self.word_freq = deepcopy(self.pipeline.token_freq)
        print(self.word_freq)

        # step 5-1
        # word freq for title only
        self.pipeline \
            .tokenize(self.title_list) \
            .remove_words_from_token_list(self.excludes) \
            .keep_words_from_token_list(self.custom_words) \
            .count_tokens()
        self.title_word_freq = deepcopy(self.pipeline.token_freq)

        # step 5-2
        # if an article's title contains a keyword,
        # add number of pushes of this article to this keyword
        self.title_word_freq = dict(self.title_word_freq)
        for key, _ in self.title_word_freq.items():
            for article in self.parser.get_articles():
                if key in article.title:
                    self.title_word_freq[key] += article.push_count

        # step 5-3
        # sort title_word_freq
        self.title_word_freq = sorted(self.title_word_freq.items(), key=lambda x: x[1], reverse=True)
        print(self.title_word_freq)

from abc import ABC
from datetime import datetime

class NlpPipeline(ABC):

    def __init__(self):
        self.custom_dict = None
        self.token_list = None
        self.pos_list = None
        self.ner_list = None
        self.token_freq = None
        print('==> nlp pipeline init!')
        self.special_words = ['GG', 'gg', '台GG', '台gg', '發哥', '99', '台積', '台積電', 'XD', 'XDD', 'XDDD', 'XDDDD', 'XDDDDD']

    def set_custom_dict(self, *args):
        raise Exception('Not Implemented Yet')

    def tokenize(self):
        raise Exception('Not Implemented Yet')

    def tag_pos(self):
        raise Exception('Not Implemented Yet')

    def tag_ner(self):
        raise Exception('Not Implemented Yet')

    def remove_punctuations_from_token_list(self):
        raise Exception('Not Implemented Yet')

    def remove_words_from_token_list(self, words):
        if self.token_list is None:
            raise Exception('token list is None, tokenize() should be called first')

        _token_list = []

        for i, _ in enumerate(self.token_list):
            _token_list.append([])
            for token in self.token_list[i]:
                if token not in words:
                    _token_list[i].append(token)
        self.token_list = _token_list
        return self

    def keep_words_from_token_list(self, words):
        if self.token_list is None:
            raise Exception('token list is None, tokenize() should be called first')

        _token_list = []

        for i, _ in enumerate(self.token_list):
            _token_list.append([])
            for token in self.token_list[i]:
                if len(token) <= 1:
                    continue
                elif token in words:
                    _token_list[i].append(token)
        self.token_list = _token_list
        return self

    def count_tokens(self):
        if self.token_list is None:
            raise Exception('token list is None, tokenize() should be called first')

        self.token_freq = {}

        for i, _ in enumerate(self.token_list):
            for token in self.token_list[i]:
                if token not in self.token_freq:
                    self.token_freq[token] = 1
                else:
                    self.token_freq[token] += 1
        # after sorting, dict would became list
        self.token_freq = sorted(self.token_freq.items(), key=lambda x: x[1], reverse=True)
        return self

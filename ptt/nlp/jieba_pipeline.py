from .nlp_pipeline import NlpPipeline
import jieba
import os
import csv

class JiebaPipeline(NlpPipeline):

    def __init__(self):

        super().__init__()

        # load default dictionary
        self.dict_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jieba', 'dict.txt.big')
        jieba.set_dictionary(self.dict_path)

        # custom (stock symbols) dictionary would be generated runtime
        self.custom_dict_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jieba', 'user_dict.txt')

        print('==> jieba pipeline init!')

    def __construct_dictionary(self, _dict):
        print(f'construct custom dict, dict size = {len(_dict)}')
        with open(self.custom_dict_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ')
            for key, value in _dict.items():
                writer.writerow([key, value])

    def set_custom_dict(self, arr):
        tmp_dict = {}
        for word in arr:
            tmp_dict[word] = 2000
        # special words
        for word in self.special_words:
            tmp_dict[word] = 9999
        self.__construct_dictionary(tmp_dict)
        jieba.load_userdict(self.custom_dict_path)
        return self

    def tokenize(self, input_list):
        print(f'==> tokenize start ...')

        self.token_list = []
        for input in input_list:
            self.token_list.append(list(jieba.cut(input)))

        print(f'==> tokenize done !')
        return self

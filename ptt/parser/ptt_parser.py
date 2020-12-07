import datetime
from datetime import timedelta
import requests
from lxml import etree
from time import sleep
import re

class Today():

    def __init__(self):
        date = datetime.datetime.today() # - timedelta(days=21)
        self.month = str(date.month) if date.month >= 10 else ' ' + str(date.month)
        self.day = str(date.day) if date.day >= 10 else '0' + str(date.day)
        self.date = self.month + '/' + self.day

    def equal_to(self, another_date):
        if self.date == another_date:
            return True
        else:
            return False

class PttArticle():

    def __init__(self, title, href):
        self.title = re.sub(r'\[.+\]|Re:|Fw:', '', title).strip()
        self.href = href
        self.date = ''
        self.push_count = 1
        self.content = []
        self.pushes = []

    def set_date(self, date):
        self.date = date

    def set_push_count(self, push_count):
        try:
            self.push_count = int(push_count)
        except ValueError:
            if push_count == '爆':
                self.push_count += 99
            elif 'X' in push_count:
                for c in push_count:
                    if c == 'X':
                        self.push_count *= 10
                    else:
                        self.push_count *= int(c)

    def set_content(self, content):
        for c in content:
            arr = re.split(r'[,，。:：;；?？!！\n]', c.replace(': ', '').strip())
            for ele in arr:
                ele = re.sub(r'[\n]{2,}', '\n', ele).replace(': ', '').strip()
                if len(ele) != 0:
                    self.content.append(ele)

    def add_push(self, push):
        self.pushes.append(push.replace(': ', '').strip())

class PttBoard():

    base_url = 'https://www.ptt.cc'

    def __init__(self, board, today):
        self.board = board
        self.today = today
        self.first_page_url = 'https://www.ptt.cc/bbs/{}/index.html'.format(board)
        self.next_page_url = None
        self.current_page_url = self.first_page_url
        self.articles = []
        self.parse_pages()

    def is_removed_article(self, entry):
        # if entry has no child node, it's been removed
        if len(entry) == 0:
            return True
        # if entry has child nodes, we can parse title and href from it
        else:
            return False

    # check if today's articles are all parsed
    def are_all_prev_days_articles(self, dates):
        for date in dates:
            if self.today.equal_to(date):
                return False
        return True

    def parse_pages(self):
        while self.current_page_url:
            # get page
            print('==> parse page: {}'.format(self.current_page_url))
            resp = requests.get(self.current_page_url)
            content = resp.text
            tree = etree.HTML(content)

            # parse entries & dates for each article
            entries = tree.xpath("//div[contains(@class, 'title')]")
            dates = tree.xpath("//div[contains(@class, 'meta')]/div[contains(@class, 'date')]/text()")
            rec_counts = tree.xpath("//*[@class='nrec']")
            print('    get {} articles'.format(len(entries)))

            # today's articles are all parsed
            if self.are_all_prev_days_articles(dates):
                self.next_page_url = None
            # continue parsing today's articles and get next page url
            else:
                for child_nodes, date, rec_count in zip(entries, dates, rec_counts):
                    if self.is_removed_article(child_nodes):
                        # empty title entry, this article has been removed
                        continue
                    elif self.today.equal_to(date):
                        article = PttArticle(child_nodes[0].text, PttBoard.base_url + child_nodes[0].get('href'))
                        article.set_date(date)
                        push_count = etree.HTML(etree.tostring(rec_count)).xpath("//span/text()")
                        if len(push_count) == 0:
                            push_count = 1
                        else:
                            push_count = push_count[0]
                        article.set_push_count(push_count)
                        self.articles.append(article)
                self.next_page_url = PttBoard.base_url + tree.xpath("//*[@id='action-bar-container']/div/div[2]/a[2]")[0].get('href')

            self.current_page_url = self.next_page_url

        print('==> totally get {} articles'.format(len(self.articles)))
        self.parse_articles()

    def parse_articles(self):
        for article in self.articles:
            # get page
            print('==> parse article: {} {}'.format(article.title, article.push_count))
            resp = requests.get(article.href)
            content = resp.text
            tree = etree.HTML(content)

            # parse content for each article
            content = tree.xpath("//*[@id='main-content']/text()")
            article.set_content(content)

            # parse pushes for each article
            pushes = tree.xpath("//*[@id='main-content']/div[@class='push']/span[contains(@class, 'push-content')]/text()")
            for push in pushes:
                article.add_push(push)

            sleep(2)

    def get_articles(self):
        return self.articles

class PttParser():

    def __init__(self, board):
        self.board = PttBoard(board, Today())

    def get_articles(self):
        return self.board.get_articles()

    def get_title_list(self):
        res = []
        for article in self.board.get_articles():
            res.append(article.title)
        return res

    def get_sentence_list(self):
        res = []
        for article in self.board.get_articles():
            res.append(article.title)
            res.extend(article.content)
            res.extend(article.pushes)
        return res

    def get_pushes_list(self):
        res = []
        for article in self.board.get_articles():
            res.extend(article.pushes)
        return res

    def get_sentence_list_without_content(self):
        res = []
        for article in self.board.get_articles():
            res.append(article.title)
            res.extend(article.pushes)
        return res

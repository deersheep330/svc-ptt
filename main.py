from ptt.parser import PttParser

if __name__ == '__main__':

    # parse ptt articles
    parser = PttParser('Stock')
    articles = parser.get_articles()
from crawl import Crawler
from utils import createWordcloud
from preprocessing import Preprocessor

if __name__ == '__main__':
    crawler = Crawler('코로나 백신', '1020')
    result = crawler.run()

    preprocessor = Preprocessor(titles=result)
    data = preprocessor.getMostUsedWords()

    createWordcloud('mask.png', data)


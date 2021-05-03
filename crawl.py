from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import parse
import time

class Crawler():
    def __init__(self, keyword, newspaper):
        self.keyword = parse.quote_plus(keyword)
        self.newspaper = newspaper
        self.article_titles = []

    def setKeyword(self):
        self.keyword = keyword


    def setNewspaper(self):
        self.newspaper = newspaper


    def setUrl(self):
        keyword_blank = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={self.keyword}"
        newspaper_blank = f"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=67&mynews=0&office_type=0&office_section_code=0&news_office_checked={self.newspaper}"
        url = keyword_blank + newspaper_blank + '&nso=so:r,p:all,a:all&start={page_num}'
        return url


    def run(self):
        for num in range(1,10):
            url = self.setUrl()
            url = url.format(page_num=num)
            print(url)
            html = urlopen(url)
            self.article_titles.append(self.parseHTML(html))

        return self.article_titles
    

    def parseHTML(self, html):
        titles = []
        res = BeautifulSoup(html, 'html.parser')
        news_area = res.select('div.news_area > a')

        for news in news_area:
            titles.append(news.get('title'))

        return titles
        


    





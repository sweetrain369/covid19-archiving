from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib import parse
import time
from konlpy.tag import Okt
from preprocessing import *

from utils import dbDataSave


stopwords = ['\n','에서','미','!!','룡','여행',':','"',':','집','/','좋은','앞','-','>','<','이','?','!','(', '의','뉴','2019.10','아영','정리','혼자','17','23','?','더','라','해외관광',',','...','워','본','[',']','위','곳','/','한','에','동','가','총','07',
'.','2019.09','_','점','양','혼다','그','찌','성규',')','와','것','등']

class Crawler():
    def __init__(self, keyword, newspaper):
        self.keyword = parse.quote_plus(keyword)
        self.newspaper = newspaper
        self.news_titles = []
        self.news_urls = []
        # 코로나 -> 
        self.search_urls = []


    def setKeyword(self):
        self.keyword = keyword


    def setNewspaper(self):
        self.newspaper = newspaper


    def setSearchUrl(self):
        keyword_blank = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={self.keyword}"
        newspaper_blank = f"&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=67&mynews=1&office_type=1&office_section_code=1&news_office_checked={self.newspaper}"
        url = keyword_blank + newspaper_blank + '&nso=so:r,p:all,a:all&start={page_num}'
        
        return url


    def getSearchUrl(self):
        hrefs = []
        for num in range(0,100):
            url = self.setSearchUrl()
            url = url.format(page_num=str(num)+'1')
            req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
            html = urlopen(req)
            # 각 신문에 대한 링크 수집(href)
            hrefs.append(self.getNewsUrl(html)) 
        
        return hrefs
    

    def getNewsUrl(self, html):
        news_urls = []
        res = BeautifulSoup(html, 'html.parser')
        news_area = res.select('div.news_area > a')
        for news in news_area:
            news_urls.append(news.get('href'))

        return news_urls


    def getKhan(self):
        start = time.time()
    
        okt = Okt()
        hrefs = self.getSearchUrl()
        news_contents = []
        idx = 1
        error = 0
        for href in hrefs:
            for url in href:
                try:
                    req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
                    html = urlopen(req)
                    res = BeautifulSoup(html, 'html.parser')

                    # content
                    contents_elem = res.select('div#wrap > div#container > div.art_cont > div.art_body > p.content_text')
                    content = ''
                    for contents in contents_elem:
                        content = content + contents.get_text()
                    content_words = getMorphs(content)
                    content_words = filterStopwords(content_words, stopwords)
                    content_words = '+'.join(content_words)
                    # title
                    title_elem = res.select('div#wrap > div#container > div.art_header > div.subject > h1')
                    title = title_elem[0].get_text()
                    title_words = getMorphs(title)
                    title_words = filterStopwords(title_words, stopwords)
                    title_words = '+'.join(title_words)
                    # date 
                    date_elem = res.select('div#wrap > div#container > div.art_header > div.function_wrap > div.pagecontrol > div.byline > em')
                    date = date_elem[0].get_text().split(" ")[2]
                    #print(idx)

                    tp = (idx, url, date, title, content, title_words, content_words)
                    dbDataSave(tp)
                    #print('success ')

                    idx = idx + 1
            
                except IndexError as e:
                    error = error + 1
                    #print('title : ', title)
                except KeyError as e:
                    error = error + 1


        print('time :', time.time() - start) # 현재 시각 - 시작 시간 = 실행 시간
        print('error : ', error)




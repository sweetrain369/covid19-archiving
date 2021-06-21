from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib import parse
import time
from konlpy.tag import *
from preprocessing import *

from utils import dbDataSave


news_id = {
    '경향신문' : 1032,
    '국민일보' : 1005,
    '내일신문' : 2312,
    '동아일보' : 1020,
    '매일일보' : 2385,
    '문화일보' : 1021,
    '서울신문' : 1081,
    '세계일보' : 1022,
    '아시아투데이' : 2268,
    '전국매일신문' : 2844,
    '조선일보' : 1023,
    '중앙일보' : 1025,
    '천지일보' : 2041,
    '한겨례' : 1028,
    '한국일보' : 1469
}

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


    # 일주일 건수 구할 때 사용하는 setUrl
    def setSearchUrl(self):
        keyword_blank = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={self.keyword}"
        newspaper_blank = f"&sort=0&photo=0&field=0&pd=1&ds=&de=&cluster_rank=67&mynews=1&office_type=1&office_section_code=1&news_office_checked={self.newspaper}"
        url = keyword_blank + newspaper_blank+ '&nso=so:r,p:1w,a:all&start={page_num}'
        
        return url

    # default
    def setDefaultSearchUrl(self):
        keyword_blank = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={self.keyword}"
        newspaper_blank = "&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=67&mynews=1&office_type=1&office_section_code=1&news_office_checked={newspaper}"
        url = keyword_blank + newspaper_blank + '&nso=so:r,p:all,a:all&start={page_num}'

        return url


    def getSearchUrl(self):
        hrefs = []
        for num in range(0,2):
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

    # 경향 신문
    def getNewsKhan(self):
        titles = []
        start = time.time()
        #keyword = 
        komoran = Komoran()
        hrefs = self.getSearchUrl()
        #idx = 1891
        error = 0
        for href in hrefs:
            for url in href:
                try:
                    if url == 'http://news.khan.co.kr/kh_news/khan_art_view.html?artid=20210416':
                        continue
                    #print(url)
                    req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
                    html = urlopen(req)
                    res = BeautifulSoup(html, 'html.parser')

                    # content
                    # contents_elem = res.select('div#wrap > div#container > div.art_cont > div.art_body > p.content_text')
                    # content = ''
                    # for contents in contents_elem:
                    #     content = content + contents.get_text()
                    # content_words = getMorphs(content)
                    # content_words = filterStopwords(content_words, stopwords)
                    # content_words = '+'.join(content_words)
                    # title

                    title_elem = res.select('div#wrap > div#container > div.art_header > div.subject > h1')
                    title = title_elem[0].get_text()
                    titles.append(title)
                    # title_words = getMorphs(title)
                    # title_words = filterStopwords(title_words, stopwords)
                    # title_words = '+'.join(title_words)

                    # date 
                    # date_elem = res.select('div#wrap > div#container > div.art_header > div.function_wrap > div.pagecontrol > div.byline > em')
                    # date = date_elem[0].get_text().split(" ")[2]

                   # tp = (idx, keyword, url, date, title, content, title_words, content_words)
                   # dbDataSave(tp)

                    idx = idx + 1
                
                except IndexError:
                    print('!!!!!!!!!!!!!! Index Error !!!!!!!!!!!!')
                    #print(title)
                except Exception as e:
                     print(e)
                     #print(title)
                     error = error + 1

        print('time :', time.time() - start) # 현재 시각 - 시작 시간 = 실행 시간
        print('error : ', error)

        return titles

    # 아시아투데이 신문
    def getNewsAsiaToday(self):
        hrefs = self.getSearchUrl(news_id, '아시아투데이')
        for href in hrefs:
            for url in href:
                try:
                    req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
                    html = urlopen(req)
                    res = BeautifulSoup(html, 'html.parser') 
                    # content
                    contents_elem = res.select('#section_main > div.article_box > dl.article_body > div.news_bm')
                    content = ''
                    for contents in contents_elem:
                        content = content + contents.get_text()
                    print('content : ', content)
                except Exception as e:
                    print(e)

    
    # 일주일에 몇건인지 세어주는 함수
    def getWeekNewsCnt(self, news_id):
        for key, val in news_id.items():
            print(key)
            num = 0
            while True:
                url = self.setSearchUrl()
                url = url.format(page_num=str(num)+'1', keyword=self.keyword, newspaper=val)
                #print(url)
                req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
                html = urlopen(req) 
                res = BeautifulSoup(html, 'html.parser') 
                con = res.select('#main_pack > div.api_sc_page_wrap > div > a.btn_next')[0]['aria-disabled'] # 다음 버튼
                # 마지막 페이지의 뉴스 개수 세기
                if con == 'true':
                    cnt = 0
                    ul = res.select('#main_pack > section.sc_new.sp_nnews.sp_nnews_v1._prs_nws > div > div.group_news > ul')
                    for _ in ul[0].find_all('li', {'class' : 'bx'}):
                        cnt += 1
                    break
                num += 1
            total = (num * 10) + cnt
            print(key +' 의 일주일 간 총 뉴스 기사 건수는 ? ', total)
        

    



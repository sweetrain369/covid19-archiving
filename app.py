from crawl import Crawler
from utils import createWordcloud
from preprocessing import Preprocessor

from flask import Flask, render_template, request
import time
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')


# @app.route('/post', methods=['POST', 'GET'])
# def Post():
    # crawler = Crawler('코로나19', '1032')
    # result = crawler.run()

    # preprocessor = Preprocessor(titles=result)
    # data = preprocessor.getMostUsedWords()

    # wc = createWordcloud('hospital.png', data)

    # wc.to_file(filename="wordcluoud.png")
    
    # return result


if __name__ == '__main__':
    #app.run(debug=True)
    crawler = Crawler('코로나19', '1032')
    #result = crawler.run()
    content = crawler.getKhan()
    #
    
    start = time.time()
    print('time :', time.time() - start) # 현재 시각 - 시작 시간 = 실행 시간
    
    

    # crawler = Crawler('코로나19', '1032')
    # #result = crawler.run()
    # content = crawler.getKhan()
    # print(content)
    
    

    

    
    
    


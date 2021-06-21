from crawl import Crawler, news_id
from utils import createWordcloud, loadContentWord, readyWordcloud
from preprocessing import Preprocessor

from flask import Flask, render_template, request, send_file
import time
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')



@app.route('/keyword', methods=['POST', 'GET'])
def Post():
    keyword = request.form['name']
    crawler = Crawler(keyword, '1032')
    result = crawler.getNewsKhan()

    preprocessor = Preprocessor(titles=result)
    data = preprocessor.getMostUsedWords()
    # 워드 클라우드 생성
    createWordcloud('hospital.png', data, keyword)



#@app.route('/wordcloud', methods=['POST', 'GET'])
# def image_load(keyword):
#     print('!!!!!!!!!!!')
#     #image = request.form['image_path']
#     keyword += '.png'
#     print(keyword)
#     return render_template('showImage.html', image_file = keyword )



if __name__ == '__main__':
    app.run(debug=True)
    #crawler = Crawler('코로나19')
    #crawler.getNewsAsiaToday()
    #crawler.getWeekNewsCnt(news_id);
    # 워드 클라우드를 그릴 단어들을 DB에서 꺼내서 전처리 (List에 담는 과정), 그리고 나서 List를 리턴함
    # words = loadContentWord()
    # word_list = readyWordcloud(words)
    # # 워드 클라우드 생성
    # createWordcloud('hospital.png', word_list)





    
    

    

    
    
    


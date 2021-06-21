from matplotlib import font_manager, rc

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from wordcloud import ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
import pymysql


con = pymysql.connect(host='203.234.62.172', user = 'root', password = 'ami1223', db = 'covid19_news', charset = 'utf8')

def setHangulFont():
    path="c:/Windows/Fonts/malgun.ttf"
    if platform.system()=='Darwin':
        rc('font', family='AppleGothic')
    elif platform.system()== 'Windows':
        font_name=font_manager.FontProperties(fname=path).get_name()
        rc('font', family=font_name)
    else:
        print('Unknown system... sorry~')
    plt.rcParams['axes.unicode_minus']=False


def createWordcloud(mask_path, data, keyword):
    mask = np.array(Image.open(mask_path))
    image_colors = ImageColorGenerator(mask)

    wc = WordCloud(font_path="C:\Windows\Fonts\\malgun.TTF", relative_scaling=0.1, background_color='white' ,min_font_size=1, max_font_size=100, mask=mask).generate_from_frequencies(dict(data))

    """plt.figure(figsize=(12,12))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    """
    wc.to_file(keyword + '.png')


def loadContentWord():
    cur = con.cursor()
    cur.execute("SELECT content_words FROM navernews WHERE keyword = '코로나19'")
    results = cur.fetchall()
    cur.close()
    return results


def dbDataSave(tp):
    cur = con.cursor()
    #print(tp)
    cur.execute("INSERT INTO navernews (idx, keyword, url, date, title, content, title_words, content_words) values (%s, %s, %s, %s, %s, %s, %s, %s)", tp)
    con.commit()
    cur.close()
    

def readyWordcloud(results):
    text = ''
    List = []
    for result in results:
        for i in result:
            texts = i.split('+')
            for text in texts:
                print(text)
                List.append(text)
    return List


#def readyWordcloud()

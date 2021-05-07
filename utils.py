from matplotlib import font_manager, rc

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from wordcloud import ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
import pymysql


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


def createWordcloud(mask_path, data):
    mask = np.array(Image.open(mask_path))
    image_colors = ImageColorGenerator(mask)

    wc = WordCloud(font_path="C:\Windows\Fonts\\malgun.TTF", relative_scaling=0.1, background_color='white' ,min_font_size=1, max_font_size=100, mask=mask).generate_from_frequencies(dict(data))

    plt.figure(figsize=(12,12))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    
    image_path = 'wordcloud/wordcloud.png'
    plt.saveimg(image_path)
    return image_path


#def showWordcloud(image_path):
    

def dbDataSave(tp):
    con = pymysql.connect(host='203.234.62.172', user = 'root', password = 'ami1223', db = 'covid19_news', charset = 'utf8')
    cur = con.cursor()
    #print(tp)
    cur.execute("INSERT INTO navernews (idx, url, date, title, content, title_words, content_words) values (%s, %s, %s, %s, %s, %s, %s)", tp)
    con.commit()
    cur.close()
    

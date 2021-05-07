from konlpy.tag import Okt
import nltk



class Preprocessor():
    def __init__(self, titles):
        self.titles = titles
        self.full_titles = ''
        self.stopwords = ['\n','에서','미','!!','룡','여행',':','"',':','집','/','좋은','앞','-','>','<','이','?','!','(', '의','뉴','2019.10','아영','정리','혼자','17','23','?','더','라','해외관광',',','...','워','본','[',']','위','곳','/','한','에','동','가','총','07',
        '.','2019.09','_','점','양','혼다','그','찌','성규',')','와']
        self.tokens_ko = []
        self.data = ''


    def tokensOneLine(self):
        for title in self.titles:
            for each_line in title:
                self.full_titles = self.full_titles + each_line + '\n' 
        return self.full_titles


    def tokenText(self):
        okt = Okt()
        self.full_titles = self.tokensOneLine()
        self.tokens_ko = okt.morphs(self.full_titles)
        return self.tokens_ko


    def filterStopwords(self):
        self.tokens_ko = self.tokenText()
        self.tokens_ko = [each_word for each_word in self.tokens_ko if each_word not in self.stopwords]
        return self.tokens_ko


    def getMostUsedWords(self):
        self.tokens_ko = self.filterStopwords()
        ko = nltk.Text(self.tokens_ko, name='covid 뉴스 기사 상위 단어 100개')
        self.data = ko.vocab().most_common(200)
        return self.data



def getMorphs(text):
    okt = Okt()
    return okt.nouns(text)

def filterStopwords(tokens_ko, stopwords):
    tokens_ko = [each_word for each_word in tokens_ko if each_word not in stopwords]
    return tokens_ko




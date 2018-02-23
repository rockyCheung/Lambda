# -*- coding:utf-8 -*-
import jieba
import jieba.posseg as pseg
import re
import sys
from cobra.conf.GlobalSettings import *
import nltk
#jieba 分词可以将我们的自定义词典导入，格式 “词” “词性” “词频”
jieba.load_userdict(JIEBA_USER_DICT)

#定义一个keyword类
class KeywordCuttingMachine(object):

    def __init__(self):
        # self.filename = filename
        reload(sys)
        sys.setdefaultencoding('utf8')
        pass

    #加载停用词库
    def chineseStopwords(self):          #导入停用词库
        stopword=[]
        cfp=open(JIEBA_STOP_WORDS,mode='r')#,'r+','utf-8')   #停用词的txt文件
        for line in cfp:
            for word in line.split():
                stopword.append(word)
        cfp.close()
        return stopword

    ###################################################################################################
    # 去除内容的空格、标点、数字、特色字符
    ###################################################################################################
    def deleSpecialChar(self,sentenceData):
        # 利用正则表达式去掉一些一些标点符号之类的符号。
        sentenceData = re.sub(r'\s+', ' ', sentenceData)  # trans 多空格 to空格
        sentenceData = re.sub(r'\n+', ' ', sentenceData)  # trans 换行 to空格
        sentenceData = re.sub(r'\t+', ' ', sentenceData)  # trans Tab to空格
        sentenceData = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——；！，”。《》，。：“？、~@#￥%……&*（）1234567①②③④)]+". \
                              decode("utf8"), "".decode("utf8"), sentenceData)
        return sentenceData
    ###################################################################################################
    # 去除内容的空格、标点、数字、特色字符,进行分词，并去除停用词
    ###################################################################################################
    def wordsCutting(self, sentenceData):
        wordlist = list(jieba.lcut(sentenceData))  # jieba.cut  把字符串切割成词并添加至一个列表
        wordlistN = []
        chineseStopwords = self.chineseStopwords()
        for word in wordlist:
            temp = word.decode("utf-8")
            if temp not in chineseStopwords:  # 词语的清洗：去停用词
                if temp != '\r\n' and temp != ' ' and temp != '\u3000'.decode('unicode_escape') \
                        and temp != '\xa0'.decode('unicode_escape'):  # 词语的清洗：去全角空格
                    wordlistN.append(word)
        return wordlistN

    ###################################################################################################
    # 提取名词
    ###################################################################################################
    def nounExtract(self, sentenceData):  # 名词提取函数
        words = pseg.cut(sentenceData)
        wordLsist = []
        for wds in words:
            # 筛选自定义词典中的词，和各类名词，自定义词库的词在没设置词性的情况下默认为x词性，即词的flag词性为x
            if wds.flag == 'x' and wds.word != ' ' and wds.word != 'ns' \
                    or re.match(r'^n', wds.flag) != None \
                            and re.match(r'^nr', wds.flag) == None:
                wordLsist.append(wds.word)
        return wordLsist

    ###################################################################################################
    # 排序
    ###################################################################################################
    def sortItem(self, item):  # 排序函数，正序排序
        vocab = []
        for k, v in item:
            vocab.append((k, v))
        resultList = list(sorted(vocab, key=lambda v: v[1], reverse=1))
        return resultList

    ###################################################################################################
    # 分词处理
    ###################################################################################################
    def doCutting(self,content):
        # Apage = open(self.filename, 'r+', 'utf-8')
        # Word = Apage.read()  # 先读取整篇文章
        noun = self.nounExtract(content)  # 对整篇文章进行词性的挑选
        tempString = ''.join(noun)
        resultList = self.wordsCutting(tempString)  # 对挑选后的文章进行分词
        # Apage.close()
        return resultList


# ss = KeywordCuttingMachine()
# sentenceData = ss.deleSpecialChar('在使用这个语料库之前，我们首先要检查一下是否已经安装了这个语料库。')
# print sentenceData
# result = ss.doCutting(sentenceData)
# print result
# for i in result:
#     print i.decode("utf-8")
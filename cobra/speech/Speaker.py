# -*- coding:utf-8 -*-

from textblob import TextBlob
import pyttsx3


class Speaker(object):

    def __init__(self):
        self.engine = pyttsx3.init()

    #######
    # lang zh-CN en
    #####
    def translate(self,text,fromLang,toLang):
        blob = TextBlob(text)
        translateText = blob.translate(from_lang=fromLang,to=toLang)
        return translateText

    ####################
    # 预测语言
    ####################
    def detectLang(self,text):
        blob = TextBlob(text)
        return blob.detect_language()

    def read(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
speaker = Speaker()
# print speaker.translate(u'我是谁','zh-CN','en')
speaker.read(u"我是谁")
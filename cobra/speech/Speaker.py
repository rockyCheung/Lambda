# -*- coding:utf-8 -*-

from textblob import TextBlob
import pyttsx3
import speech_recognition as sr


class Speaker(object):

    def __init__(self):
        self.engine = pyttsx3.init()

    #######
    # 翻译lang zh-CN en
    #####
    def translate(self,text,fromLang,toLang):
        blob = TextBlob(text)
        translateText = blob.translate(from_lang=fromLang,to=toLang)
        return translateText

    ####################
    # 识别语言
    ####################
    def detectLang(self,text):
        blob = TextBlob(text)
        return blob.detect_language()

    ####################
    # 朗读
    ####################
    def read(self,text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listenMicrophone(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        # recognize speech using Sphinx
        try:
            print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

        # recognize speech using Google Speech Recognition
        # try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
        #     print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        # except sr.UnknownValueError:
        #     print("Google Speech Recognition could not understand audio")
        # except sr.RequestError as e:
        #     print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # recognize speech using Google Cloud Speech
        # GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
        # try:
        #     print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio,
        #                                                                             credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        # except sr.UnknownValueError:
        #     print("Google Cloud Speech could not understand audio")
        # except sr.RequestError as e:
        #     print("Could not request results from Google Cloud Speech service; {0}".format(e))

        # recognize speech using Wit.ai
        # WIT_AI_KEY = "INSERT WIT.AI API KEY HERE"  # Wit.ai keys are 32-character uppercase alphanumeric strings
        # try:
        #     print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
        # except sr.UnknownValueError:
        #     print("Wit.ai could not understand audio")
        # except sr.RequestError as e:
        #     print("Could not request results from Wit.ai service; {0}".format(e))

        # recognize speech using Microsoft Bing Voice Recognition
        # BING_KEY = "INSERT BING API KEY HERE"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
        # try:
        #     print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
        # except sr.UnknownValueError:
        #     print("Microsoft Bing Voice Recognition could not understand audio")
        # except sr.RequestError as e:
        #     print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

        # recognize speech using Houndify
        # HOUNDIFY_CLIENT_ID = "INSERT HOUNDIFY CLIENT ID HERE"  # Houndify client IDs are Base64-encoded strings
        # HOUNDIFY_CLIENT_KEY = "INSERT HOUNDIFY CLIENT KEY HERE"  # Houndify client keys are Base64-encoded strings
        # try:
        #     print("Houndify thinks you said " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID,
        #                                                              client_key=HOUNDIFY_CLIENT_KEY))
        # except sr.UnknownValueError:
        #     print("Houndify could not understand audio")
        # except sr.RequestError as e:
        #     print("Could not request results from Houndify service; {0}".format(e))

        # recognize speech using IBM Speech to Text
        # IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        # IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
        # try:
        #     print("IBM Speech to Text thinks you said " + r.recognize_ibm(audio, username=IBM_USERNAME,
        #                                                                   password=IBM_PASSWORD))
        # except sr.UnknownValueError:
        #     print("IBM Speech to Text could not understand audio")
        # except sr.RequestError as e:
        #     print("Could not request results from IBM Speech to Text service; {0}".format(e))

    # this is called from the background thread
    def callback(recognizer, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

speaker = Speaker()
# print speaker.translate(u'我是谁','zh-CN','en')
# speaker.read(u"我是谁")
speaker.listenMicrophone()
# r = sr.Recognizer()
# m = sr.Microphone()
# with m as source:
#     r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
#
# # start listening in the background (note that we don't have to do this inside a `with` statement)
# stop_listening = r.listen_in_background(m, callback)
# # `stop_listening` is now a function that, when called, stops background listening
#
# # do some unrelated computations for 5 seconds
# for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things
#
# # calling this function requests that the background listener stop listening
# stop_listening(wait_for_stop=False)
#
# # do some more unrelated things
# while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping

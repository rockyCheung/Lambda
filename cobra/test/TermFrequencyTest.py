from cobra.article.TermFrequency import TermFrequency

import unittest
class TestgetSimpleConsumerMethods(unittest.TestCase):
    def test_queryArticleDataFrame(self):
        term = TermFrequency(appName='article',masterName='local[1]')
        term.transformContent(dbName='lhhs',collectionName='article')
        try:
            print 'test'
            term.transformContent('lhhs', 'article')
            term.sendArticleToProducer(topic='topic_test_1')
            docs = term.queryArticles(qeury={'type':'3'},sort='type')
            for i in docs:
                print i
                articleTuple = term.queryArticleDataFrame(dbName='lhhs', collectionName='article_text')
                articleTuple.show(n=20, truncate=True)
            term.featureExtract(articleTuple,articleTuple)
            term.caculatTermFrequency(articleTuple)
        except Exception,e:
            raise e
        finally:
            term.stopSpark()
if __name__ == '__main__':
    unittest.main()
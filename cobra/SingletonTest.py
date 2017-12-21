from pyspark import SparkContext, SparkConf

class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class MyClass(Singleton):
    a = 1
    def __init__(self,name):
        self.name = name
        self.conf = SparkConf().setAppName("test").setMaster("local")
    def p(self):
        print self.name
#
# one = MyClass("rocky")
# two = MyClass("rocky1")
# print one == two,one is two
# one.p()
# two.p()
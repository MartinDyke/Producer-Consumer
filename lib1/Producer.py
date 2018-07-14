from lib1.Quote import *

class Producer:
    def __init__(self, buff, companies):
        self.buffer = buff
        self.companies = companies

    def getRandomQuote(self):
        return Quote(self.companies)

    def run(self):
        for i in range(100000):
            self.buffer.add(self.getRandomQuote())
import statistics
import random
import timeit
import multiprocessing
from threading import Thread


# What defines what a quote is?
# - The logic of getRandomQuote() is fine but it should return a concrete object of type Quote.
# - There is nothing stopping somebody building on top of your Producer class and changing for example, the order of the
#   quote items eg: [random.randint(1, 100), self.companies[random.randint(0, len(self.companies) - 1)]]. With a defined
#   quote class you are defining and enforcing what it means to be a quote to everybody else.

class Quote:
    def __init__(self, companies):
        self.company = companies[random.randint(0,len(companies)-1)]
        self.value = random.randint(0,5000)/10.0
        

class Producer:
    def __init__(self, buff, companies):
        self.buffer = buff
        self.companies = companies

    def getRandomQuote(self):
        return Quote(self.companies)

    def run(self):
        for i in range(100000):
            self.buffer.add(self.getRandomQuote())


class Buffer:
    def __init__(self):
        self.quotes = []  # quotes to be stored in list in format [['GOOG',15],['AMAZ',20],...]

    # Why do your add and remove methods guarantee that the quotes will be consumed in the same order that they were
    # produced? The impl is fine (for now) but why does it work? What are append and remove doing underneath?

    def add(self, quote):
        self.quotes.append(quote)

    def remove(self):
        res = self.quotes[0]
        self.quotes.remove(self.quotes[0])
        return res

    def isEmpty(self):
        return self.quotes == []


class Consumer:
    def __init__(self, buff, companies,file):
        self.buffer = buff  # initializes a buffer attribute buff
        self.values = {i: [0,100,0,0] for i in
                       companies}  # [counter, min, average,max]
        self.companies = companies
        self.printer = Printer(file)
    def reset(self):
        self.values= {i: [0,100,0,0] for i in self.companies}

    def run(self):
        Day=1
        while Day!=101:
            quoteNo = 1
            while quoteNo != 1000:
                if not self.buffer.isEmpty():
                    a = self.buffer.remove()
                    self.values[a.company][0] +=1
                    self.values[a.company][2] += a.value
                    if a.value < self.values[a.company][1]: self.values[a.company][1]=a.value
                    if a.value > self.values[a.company][3]: self.values[a.company][3]=a.value
                    quoteNo += 1
            self.printer.printToFile('Day ' + str(Day) + ":\n\n")
            for key in self.values:
                if self.values[key][0] !=0:
                    self.printer.printToFile('The highest value for ' + key + ' is ' + str(self.values[key][3]) + "\n" +
                                             'The lowest value for ' + key + ' is ' + str(self.values[key][1]) + "\n" +
                                             'The average value for ' + key + ' is ' + str("{0:.1f}".format(self.values[key][2]/self.values[key][0])) + '\n\n\n' )
            Day+=1
            self.reset()
        
      
class Printer:
    def __init__(self,file):
        self.file = file
    
    def printToFile(self,text):
        open(self.file,"a").write(text)
    

if __name__ == "__main__":
    T1 = timeit.default_timer()
    b = Buffer()
    comp = ['AAPL', 'AMZN', 'GOOG', 'FB', 'CSCO', 'CMCSA', 'AMGN', 'ADBE', 'GILD', 'COST']
    p = Producer(b, comp)
    c = Consumer(b, comp,"Output.txt")
    t1 = Thread(target=p.run)
    t2 = Thread(target=c.run)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    T2 = timeit.default_timer()
    print("Total elapsed time is " + str(T2 - T1))

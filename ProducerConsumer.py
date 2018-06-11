import random
import time
import timeit
from threading import Thread

# Avg runtime: 1.572

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
        while Day!=11:  # for 100 days do:
            quoteNo = 0
            while quoteNo != 2500:  # while quoteNo is less than 1000 do:
                if not self.buffer.isEmpty():
                    a = self.buffer.remove()
                    self.values[a.company][0] +=1
                    self.values[a.company][2] += a.value
                    if a.value < self.values[a.company][1]: self.values[a.company][1]=a.value
                    if a.value > self.values[a.company][3]: self.values[a.company][3]=a.value
                    quoteNo += 1
            # self.printer.printToFile('Day ' + str(Day) + "\n")
            # for key in self.values:
            #      if self.values[key][0] !=0:
            #          self.printer.printToFile('The highest value for ' + key + ' is ' + str(self.values[key][3]) + "\n" +
            #                                   'The lowest value for ' + key + ' is ' + str(self.values[key][1]) + "\n" +
            #                                   'The average value for ' + key + ' is ' + str("{0:.1f}".format(self.values[key][2]/self.values[key][0])) + '\n' )
            #
            # Print to console:
            # print('Day ' + str(Day) + ":\n")
            # for key in self.values:
            #      if self.values[key][0] != 0:
            #          print('The highest value for ' + key + ' is ' + str(self.values[key][3]) + "\n" +
            #                                   'The lowest value for ' + key + ' is ' + str(self.values[key][1]) + "\n" +
            #                                   'The average value for ' + key + ' is ' + str(
            #              "{0:.1f}".format(self.values[key][2] / self.values[key][0])) + '\n')
            
            time.sleep(0.001)
            Day+=1
            self.reset()
        
      
class Printer:
    def __init__(self,file):
        self.file = file
    
    def printToFile(self, text):
        open(self.file,"a").write(text)
    

if __name__ == "__main__":
    b = Buffer()
    comp = ['AAPL', 'AMZN', 'GOOG', 'FB', 'CSCO', 'CMCSA', 'AMGN', 'ADBE', 'GILD', 'COST']
    p = Producer(b, comp)
    c1 = Consumer(b, comp, "Output1.txt")
    c2 = Consumer(b, comp, "Output2.txt")
    c3 = Consumer(b, comp, "Output3.txt")
    c4 = Consumer(b, comp, "Output4.txt")
    t1 = Thread(target=p.run)
    t2 = Thread(target=c1.run)
    t3 = Thread(target=c2.run)
    t4 = Thread(target=c3.run)
    t5 = Thread(target=c4.run)

    T1 = timeit.default_timer()
    t1.start()
    time.sleep(0.01)
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    T2 = timeit.default_timer()
    print("Total elapsed time is " + str(T2 - T1))

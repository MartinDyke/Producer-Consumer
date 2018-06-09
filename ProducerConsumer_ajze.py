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

class Producer:
    def __init__(self, buff, companies):
        self.buffer = buff
        self.companies = companies

    def getRandomQuote(self):
        return [self.companies[random.randint(0, len(self.companies) - 1)], random.randint(1, 100)]

    def run(self):
        for i in range(1000):
            a = self.getRandomQuote()
            self.buffer.add(a[0], a[1])


class Buffer:
    def __init__(self):
        self.quotes = []  # quotes to be stored in list in format [['GOOG',15],['AMAZ',20],...]

    # Why do your add and remove methods guarantee that the quotes will be consumed in the same order that they were
    # produced? The impl is fine (for now) but why does it work? What are append and remove doing underneath?

    def add(self, company, price):
        self.quotes.append([company, price])

    def remove(self):
        res = self.quotes[0]
        self.quotes.remove(self.quotes[0])
        return res

    def isEmpty(self):
        return self.quotes == []


class Consumer:
    def __init__(self, buff, companies):
        self.buffer = buff  # initializes a buffer attribute buff
        self.quotes = {i: [] for i in
                       companies}  # quotes to be stored in format {'GOOG':[1, 2, 3, 4], 'AMAZ': [5, 6, 7, 8],...}

    def run(self):
        # In this application, the consumer should not have (and does not need to have) any knowledge of the number of
        # items it is expected to consume. Instead of counting a hardcoded value just test against the buffer:
        # 			while !self.buffer.isEmpty()
        # What are potential problems of this new approach?
        i = 1
        while i != 1000:
            if not self.buffer.isEmpty():
                a = self.buffer.remove()
                self.quotes[a[0]].append(a[1])
                i += 1

        for key in self.quotes:
            print('The highest value for ' + key + ' is ' + str(max(self.quotes[key])))
            print('The lowest value for ' + key + ' is ' + str(min(self.quotes[key])))
            print('The average value for ' + key + ' is ' + str(int(statistics.mean(self.quotes[key]))) + '\n')


if __name__ == "__main__":
    T1 = timeit.default_timer()
    b = Buffer()
    comp = ['AAPL', 'AMZN', 'GOOG', 'FB', 'CSCO', 'CMCSA', 'AMGN', 'ADBE', 'GILD', 'COST']
    p = Producer(b, comp)
    c = Consumer(b, comp)
    t1 = Thread(target=p.run)
    t2 = Thread(target=c.run)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    T2 = timeit.default_timer()
    print("Total elapsed time is " + str(T2 - T1))

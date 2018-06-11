import time
import random
import timeit
from threading import Thread


"""A module to model the Producer-Consumer idiom"""


class Quote:
    """A class to represent a stock quote.
    Attributes:
        comp_ (list): A list of company exchange codes.
        price_ (float): A float of one decimal place precision.
    """
    def __init__(self, qcomp, qprice):
        """Quote __init__ method.
        Args:
            qcomp (list): A list of company exchange codes.
            qprice (float): A float of one decimal place precision.
        """
        self.comp_ = qcomp
        self.price_ = qprice


class Producer:
    def __init__(self, buff, companies):
        self.buffer_ = buff
        self.companies_ = companies

    def getRandomQuote(self):
        """getRandomQuote().
        Args:
            None.
        Returns:
            A Quote object initialised with a randomly selected company code and price.
        """
        q = Quote(self.companies_[random.randint(0, len(self.companies_) - 1)], random.randint(0, 5000)/10.0)
        return q

    def run(self):
        for i in range(1000000):
            self.buffer_.add(self.getRandomQuote())


class Buffer:
    def __init__(self):
        """Buffer __init__ method.
        Attributes:
            quotes_ (list): A list structure to hold quotes.
        """
        self.quotes_ = []

    def add(self, quote):
        """add()
        Add an item to the buffer.
        Args:
            quote: A quote object.
        Returns:
            None.
        """
        self.quotes_.append(quote)

    def remove(self):
        """remove()
        Remove and return an item from the buffer.
        Args:
            None.
        Returns:
            A quote object.
        """
        quote = self.quotes_[0]
        self.quotes_.remove(self.quotes_[0])
        return quote

    def isEmpty(self):
        """isEmpty()
        Returns whether or not the buffer is empty.
        Args:
            None.
        Returns:
            bool: True/False.
        """
        return self.quotes_ == []


# We are going to assume that 10000 quotes represents a day's trading activity, and at the end of each day the consumer
# will publish the day's results.
class Consumer:
    def __init__(self, buff_ref, comps, quotes_per_day):
        self.buffer_ = buff_ref
        self.day_max_ = quotes_per_day

        # We will use this to calc the real-time metrics we want. This is the point of the consumer existing.
        # It will be a dictionary of: {string : list[5]} where [0] is HI,
        # [1] is LOW, [2] is AVG, [3] is cumulative sum for a block of max 10000 quotes, [4] is quote count (max 10000)
        self.quote_stats_ = {comp: [0, 0, 0, 0, 0] for comp in comps}

        # Macros for readability
        self.HI = 0
        self.LOW = 1
        self.AVG = 2
        self.SUM = 3
        self.COUNT = 4

        # These are to help us out for demonstration, wouldn't usually use these because Prod/Cons would be intended to
        # be running forever
        self.quote_count_ = 0
        self.day_count_ = 1

    # This belongs in another class - steal it off martin
    def printDailyStats(self):
        print("DAY: {DAY_NUM}".format(DAY_NUM=self.day_count_))
        for key in self.quote_stats_:
            print("{COMP} => HI: {HI}, LOW: {LOW}, AVG: {AVG}".format(COMP=key,
                                                                      HI=self.quote_stats_[key][self.HI],
                                                                      LOW=self.quote_stats_[key][self.LOW],
                                                                      AVG=self.quote_stats_[key][self.AVG]))

    def resetStats(self):
        for key in self.quote_stats_:
            self.quote_stats_.update({key: [0, 0, 0, 0, 0]})

    def processQuote(self, quote):
        # Check end-of-day
        if self.quote_count_ == self.day_max_:
            self.printDailyStats()
            self.resetStats()
            self.quote_count_ = 0
            self.day_count_ += 1

        # Calc HI
        if self.quote_stats_[quote.comp_][self.HI] < quote.price_:
            self.quote_stats_[quote.comp_][self.HI] = quote.price_

        # Calc LOW
        if self.quote_stats_[quote.comp_][self.LOW] == 0:
            self.quote_stats_[quote.comp_][self.LOW] = quote.price_
        elif self.quote_stats_[quote.comp_][self.LOW] > quote.price_:
            self.quote_stats_[quote.comp_][self.LOW] = quote.price_

        # Calc AVG
        if self.quote_stats_[quote.comp_][self.COUNT] == 0:  # Defend against divide by 0
            self.quote_stats_[quote.comp_][self.AVG] = quote.price_
            self.quote_stats_[quote.comp_][self.SUM] = quote.price_
            self.quote_stats_[quote.comp_][self.COUNT] = 1
        else:
            self.quote_stats_[quote.comp_][self.COUNT] += 1
            self.quote_stats_[quote.comp_][self.SUM] += quote.price_
            self.quote_stats_[quote.comp_][self.AVG] = round(self.quote_stats_[quote.comp_][self.SUM] /
                                                             self.quote_stats_[quote.comp_][self.COUNT])

        # Increment quote_count
        self.quote_count_ += 1

    def run(self):
        while not self.buffer_.isEmpty():
            q = self.buffer_.remove()
            self.processQuote(q)
            del q  # Help the garbage collector recover the memory used by the quote


def doTheThing():
    b = Buffer()
    comp = ['AAPL', 'AMZN', 'GOOG', 'FB', 'CSCO', 'CMCSA', 'AMGN', 'ADBE', 'GILD', 'COST']
    p = Producer(b, comp)
    c = Consumer(b, comp, 10000)
    t1 = Thread(target=p.run)
    t2 = Thread(target=c.run)

    T1 = timeit.default_timer()
    t1.start()
    time.sleep(0.01)
    t2.start()
    t1.join()
    t2.join()
    T2 = timeit.default_timer()
    print("Total elapsed time: {TIME}".format(TIME=T2 - T1))


if __name__ == "__main__":
    doTheThing()

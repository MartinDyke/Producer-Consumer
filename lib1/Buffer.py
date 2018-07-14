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
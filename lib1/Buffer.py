class Buffer:
    def __init__(self):
        #initialize buffer with storage for quotes
        self.quotes = []

    def add(self, quote):
	    #Append a new quote to the end of the buffer
		self.quotes.append(quote)

    def remove(self):
	    #Safe removal of quote from buffer operating on first in first out principle
        res = self.quotes[0]
        self.quotes.remove(self.quotes[0])
        return res

    def isEmpty(self):
	    #Check if buffer is empty
        return self.quotes == []
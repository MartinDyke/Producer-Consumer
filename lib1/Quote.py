import random

class Quote:
    def __init__(self, companies):
        self.company = companies[random.randint(0,len(companies)-1)]
        self.value = random.randint(0,5000)/10.0

    def __repr__(self):
        return 'Quote(%r, %r)' % (self.company, self.value)
#Main program start point, currently produces random quotes for ten companies, writing the results
#to .txt files. Using one producer and four consumers running on different threads.

#TO DO:
# 1. Model the quotes more realistically. Perhaps rather than random, using brownian motion.
# 2. Ensure program is more robust and consumers can crash out unexpectedly, or use up the buffer but not terminate.
# 3. Finish writing tests.

import timeit
from threading import Thread
from lib1.Producer import *
from lib1.Buffer import *
from lib1.Consumer import *


if __name__ == "__main__":
    
    #Initialize a buffer for all consumers and producer to use, as well as the list of companies
    b = Buffer()
    comp = ['AAPL', 'AMZN', 'GOOG', 'FB', 'CSCO', 'CMCSA', 'AMGN', 'ADBE', 'GILD', 'COST']
    
    #Create the producer and consumers. Results are to be output to .txt files. All using the same buffer
    p = Producer(b, comp)
    c1 = Consumer(b, comp, "Output1.txt")
    c2 = Consumer(b, comp, "Output2.txt")
    c3 = Consumer(b, comp, "Output3.txt")
    c4 = Consumer(b, comp, "Output4.txt")
    
    #Initialize threads for each of the consumers and for the producer
    t1 = Thread(target=p.run)
    t2 = Thread(target=c1.run)
    t3 = Thread(target=c2.run)
    t4 = Thread(target=c3.run)
    t5 = Thread(target=c4.run)

    T1 = timeit.default_timer()
    
    #Start all threads and wait for them to join. Producer given a 0.01s lead in order to write quotes into
    #buffer so that the consumers don't immediately terminate.
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

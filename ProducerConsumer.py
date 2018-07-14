import timeit
from threading import Thread
from lib1.Producer import *
from lib1.Buffer import *
from lib1.Consumer import *


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

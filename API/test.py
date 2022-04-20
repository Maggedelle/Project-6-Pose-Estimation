import time,sched
import datetime as dt

starttime = time.time()
b = sched.scheduler(time.time, time.sleep)


s = time.time() 
def hansi(sched):
    s = time.time()
    sched.enter(0.042,1,hansi,(sched,))
    print((time.time() - s))

b.enter(0.042, 1, hansi, (b,))
b.run()
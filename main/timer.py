import time
from datetime import datetime, timedelta

print("working")

SECONDS_PER_DAY = 24 * 60 * 60

def getSeconds():
    curTime = datetime.now()
    desTime = curTime.replace(hour=2, minute=0, second=0, microsecond=0)
    delta = curTime - desTime
    skipSeconds = SECONDS_PER_DAY - delta.total_seconds()
    print ("Must sleep %d seconds" % skipSeconds)
    return skipSeconds

def timer(n):  
    while True:  
        print (time.strftime('%Y-%m-%d %X',time.localtime())  )
        time.sleep(n)
        
def begin_interval():
    print(2)
    timer(getSeconds())
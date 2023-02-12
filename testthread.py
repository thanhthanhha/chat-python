from _thread import *
import time

def print_time(ThreadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("{}: {}".format(ThreadName, time.ctime(time.time())))

try:
    start_new_thread(print_time,("Thread-1",2))
    start_new_thread(print_time,("Thread-2",2))
except:
    print("Start thread failed")

while 1:
    pass
from collections import deque
import time
import threading

de = deque()

def inc(de, num):
    de.append(num)
    if(num < 5): 
        time.sleep(0.1)
        inc(de, num + 1)
def dec(de):
    print(de.pop())
    dec(de)

t1 = threading.Thread(target=inc, args=(de, 0))

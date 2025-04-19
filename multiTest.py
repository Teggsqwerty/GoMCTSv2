from multiprocessing import *
import time

def wait(a):
    time.sleep(a)
    print("done ", a)

if __name__ == "__main__":
    for x in range(10):
        a = Process(target = wait, args=[1])
        b = Process(target = wait, args=[0.5])
        a.start()
        b.start()
        print("done main")
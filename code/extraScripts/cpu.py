fpywXimport multiprocessing
from time import sleep
import threading
import psutil
from os import getpid

def worker():
    print("worker")
    while True:
        l = (2 * 33) >> 3


cpu = multiprocessing.cpu_count()


def stop():
    time = "!edit"
    sleep(int(time))
    me = psutil.Process(getpid())
    for child in me.children():
        child.kill()


stopper = threading.Thread(target=stop)

if __name__ == '__main__':
    stopper.start()
    for i in range(cpu):
        p = multiprocessing.Process(target=worker)
        p.start()

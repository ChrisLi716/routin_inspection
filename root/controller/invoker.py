from root.controller.dispatcher import Dispatcher
import threading
from threading import Thread, Lock


class MyThread(Thread):
    __thread_lock = Lock()

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        self.__thread_lock.acquire()
        Dispatcher.assign_to_scheduler()


if __name__ == '__main__':
    while True:
        thread = MyThread("MyThread")
        thread.start()
        thread.join()

from root.controller.dispatcher import Dispatcher
import time

if __name__ == '__main__':
    Dispatcher.assign_to_scheduler()
    time.sleep(30 * 60)

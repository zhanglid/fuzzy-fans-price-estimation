from extract_page_info_by_url import set_info 
import threading
import Queue
import time
import random
from pymongo import MongoClient

QUEUE_RECORD = Queue.Queue()


class MyWoker(threading.Thread):
    def __init__(self, proxy):
        super(MyWoker, self).__init__()
        self.proxy = proxy
        self.sucCount = 0
        self.failCount = 0

    def run(self):
        global QUEUE_RECORD
        while not QUEUE_RECORD.empty():
            time.sleep(1 + random.random())
            a = QUEUE_RECORD.get()
            if not set_info(aic, a, proxy=self.proxy):
                self.failCount = self.failCount + 1
                QUEUE_RECORD.put(a)
            else:
                self.sucCount = self.sucCount + 1
                mutex.acquire()
                print a['_id'], '|suc: ', self.sucCount, ' |fail:', self.failCount, aic.find({'_id': a['_id']})[0]['title']
                mutex.release()
                QUEUE_RECORD.task_done()
            if self.failCount > 10 and self.sucCount == 0:
                return


def show_left_num(aic):
    while True:
        time.sleep(1)
        mutex.acquire()
        print aic.count({'isGot': False})
        mutex.release()

if __name__ == '__main__':
    # start client connection
    client = MongoClient('localhost', 27017)
    # get the info of the database
    db = client.art_work_database
    aic = db.art_work_collection
    for a in aic.find({'isGot': False}):
        QUEUE_RECORD.put(a)
    threadList = []
    mutex = threading.Lock()
    proxy_list = []
    pfile = open('verified_proxy_list.txt', 'r')
    for line in pfile:
        proxy_list.append(line.replace('\n', ''))
    pfile.close()

    for i in range(len(proxy_list)):
        thread = MyWoker(proxy_list[i])
        thread.start()
        threadList.append(thread)
    t = threading.Thread(target=show_left_num, args=(aic, ))
    t.start()
    QUEUE_RECORD.join()
    t.join()



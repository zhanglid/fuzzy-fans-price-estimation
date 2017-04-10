import requests
import threading
import time
import Queue
result_list = []
TASK_QUEUE = Queue.Queue();
url = 'http://www.google.com'
rList = []

class proxy_checker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global TASK_QUEUE
        while not TASK_QUEUE.empty():
            p = TASK_QUEUE.get()
            TASK_QUEUE.task_done()
            if self.proxy_check(p):
                rList.append(p)
                print TASK_QUEUE.qsize(), p

    def proxy_check(self, p):
        try:
            requests.get(url, proxies={"http": p}, timeout=5)
        except:
            # print 'error: ', p
            i = 1
        else:
            return True
proxy_list = []
proxy_file = open('proxy.txt', 'r')

for line in proxy_file:
    proxy_list.append(line.replace('\n',''))

for p in proxy_list:
    TASK_QUEUE.put(p)
thread_list = []
for i in range(1024):
    thread = proxy_checker()
    thread.start()
    thread_list.append(thread)

for t in thread_list:
    t.join()

with open('verified_proxy_list.txt', 'w+') as vpl:
    for p in rList:
        print p
        vpl.write(p+'\n')

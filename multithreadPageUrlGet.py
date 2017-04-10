import threading
import re
import Queue
import time
import random
import requests
from bs4 import BeautifulSoup
urlList = []
_WORK_THREAD_NUM = 1
SHARE_PAGE_Q = Queue.Queue()


class PageThread(threading.Thread):
    def __init__(self, id, proxy):
        super(PageThread, self).__init__()
        self.id = id
        self.proxy = proxy

    def run(self):
        global SHARE_PAGE_Q
        success = 0
        time.sleep(random.random()*0.5*self.id)
        while not SHARE_PAGE_Q.empty():
            page_num = SHARE_PAGE_Q.get()
            SHARE_PAGE_Q.task_done()
            url = 'http://artso.artron.net/auction/search_auction.php?keyword=%E6%89%87%E9%9D%A2&page='
            time.sleep(1+random.random())
            #data = urllib2.urlopen(url + str(page_num)).read()
            try:
                rp = requests.get(url + str(page_num), proxies={"http": self.proxy})
            except:
                SHARE_PAGE_Q.put(page_num)
                continue
            time.sleep(1 + random.random())
            data = rp.content
            result_list = re.compile(r'(?:<a href=)"http://auction.artron.net/paimai-art\d+/.+(?:</a>)').findall(data)
            mutex.acquire()
            print 'id:', self.id, '|', 'num:', page_num, '|', 'result:', len(result_list)
            mutex.release()
            if len(result_list) == 0:
                time.sleep(1+random.random())
                SHARE_PAGE_Q.put(page_num)
                soup = BeautifulSoup(data, 'lxml')
                print soup.get_text()
                continue

            for s in result_list:
                page_url = re.compile(r'http://auction.artron.net/paimai-art\d+/').search(s).group()
                mutex.acquire()
                #print page_num, '|', page_url
                urlList.append(page_url)
                with open('log.txt', 'a+') as mf:
                    mf.write(page_url+'\n')
                mutex.release()


threadList = []
mutex = threading.Lock()
proxy_list = []
pfile = open('proxy.txt', 'r')
for line in pfile:
    proxy_list.append(line.replace('\n', ''))
pfile.close()

for i in range(1992):
    SHARE_PAGE_Q.put(1+i)
for i in range(len(proxy_list)):
    thread = PageThread(i, proxy_list[i])
    thread.start()
    threadList.append(thread)
SHARE_PAGE_Q.join()

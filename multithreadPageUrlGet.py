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
SOLVED_PAGE_NUM = 0;

class PageThread(threading.Thread):
    def __init__(self, id, proxy):
        super(PageThread, self).__init__()
        self.id = id
        self.proxy = proxy

    def run(self):
        global SHARE_PAGE_Q
        global SOLVED_PAGE_NUM
        success = 0
        continous_fail = 0
        time.sleep(random.random()*0.5*(self.id % 20))
        while SOLVED_PAGE_NUM != 1992:
            if SHARE_PAGE_Q.empty():
                time.sleep(0.1*random.random())
                continue
            if continous_fail > 10 and success == 0:
                return
            page_num = SHARE_PAGE_Q.get()
            SHARE_PAGE_Q.task_done()
            url = 'http://artso.artron.net/auction/search_auction.php?keyword=%E6%89%87%E9%9D%A2&page='
            time.sleep(1+random.random())
            #data = urllib2.urlopen(url + str(page_num)).read()
            headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                       #"Accept-Encoding": "gzip",
                       "Accept-Language": "zh-CN,zh;q=0.8",
                       #"Referer": "http://www.example.com/",
                       "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                       }
            try:
                rp = requests.get(url + str(page_num), proxies={"http": self.proxy}, timeout=5, headers=headers)
            except:
                SHARE_PAGE_Q.put(page_num)
                continous_fail = continous_fail + 1
                continue
            time.sleep(1 + random.random())
            data = rp.content
            result_list = re.compile(r'(?:<a href=)"http://auction.artron.net/paimai-art\d+/.+(?:</a>)').findall(data)
            if len(result_list) == 0:
                time.sleep(1+random.random())
                SHARE_PAGE_Q.put(page_num)
                #soup = BeautifulSoup(data, 'lxml')
                continous_fail = continous_fail + 1
                #print soup.get_text()[:100]
                continue
            mutex.acquire()
            SOLVED_PAGE_NUM = SOLVED_PAGE_NUM + 1
            print 'id:', self.id, '|', 'num:', page_num, '|', 'success:', success, '| failed:', continous_fail, '| result:', len(result_list), ' | ', str(SHARE_PAGE_Q.qsize()), ' | ', SOLVED_PAGE_NUM
            mutex.release()
            success = success + 1
            continous_fail = 0
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
pfile = open('verified_proxy_list.txt', 'r')
for line in pfile:
    proxy_list.append(line.replace('\n', ''))
pfile.close()

for i in range(1992):
    SHARE_PAGE_Q.put(1+i)
for i in range(len(proxy_list)):
    thread = PageThread(i, proxy_list[i])
    thread.start()
    threadList.append(thread)

for t in threadList:
    t.join()
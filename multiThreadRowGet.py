import requests
from StringIO import StringIO
from getImgRow import get_num
import threading


class myRowWorker(threading.Thread):
    def __init__(self, proxy, aic):
        super(myRowWorker, self).__init__()
        self.failCount = 0
        self.sucCount = 0
        self.aic = aic
        self.proxy = proxy

    def run(self):
        global QUEUE_RECORD
        while not QUEUE_RECORD.empty():
            time.sleep(1 + random.random())
            a = QUEUE_RECORD.get()
            if not self.set_row_info(self.aic, a):
                self.failCount = self.failCount + 1
                QUEUE_RECORD.put(a)
            else:
                self.sucCount = self.sucCount + 1
                mutex.acquire()
                print a['_id'], '|suc: ', self.sucCount, ' |fail:', self.failCount, '|row_num:', self.aic.find({'_id': a['_id']})[0][
                    'row_num'], '|unusual:', self.aic.find({'_id': a['_id']})[0]['is_row_unusual']
                mutex.release()
                QUEUE_RECORD.task_done()
            if self.failCount > 10 and self.sucCount == 0:
                return

    def set_row_info(self, a):
        if a['isGot']:
            return
        a_new = a
        url = a['img_url']
        try:
            if proxy:
                myimg_file = requests.get(url, proxies=self.proxy)
            else:
                myimg_file = requests.get(url)
        except:
            return False
        imgfile = StringIO(myimg_file.content)
        is_unusual = False
        row_num_1 = get_num(Image.open(imgfile), position=0.25, axis=1)
        row_num_2 = get_num(Image.open(imgfile), position=0.5, axis=1)
        row_num_3 = get_num(Image.open(imgfile), position=0.75, axis=1)
        if row_num_1 != row_num_2 || row_num_1 != row_num_3 || row_num_2 !=  row_num_3:
            is_unusual = True
        a_new['isGot'] = True
        info = {'row_num':row_num_2, 'is_row_unusual':is_unusual}
        a_new.update(info)
        self.aic.replace_one({'_id': a['_id']}, a_new)
        # print info
        return True

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
    QUEUE_RECORD.join()

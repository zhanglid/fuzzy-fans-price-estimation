import urllib2
import re
from bs4 import BeautifulSoup

url = 'http://artso.artron.net/auction/search_auction.php?keyword=%E6%89%87%E9%9D%A2&page='
urlList = []
for i in range(1):
    print 'page: ', i
    data = urllib2.urlopen(url+str(1+i)).read()
    resultList = re.compile(r'(?:<a href=)"http://auction.artron.net/paimai-art\d+/.+(?:</a>)').findall(data)
    soup = BeautifulSoup(data, 'lxml')
    print soup.find_all('a', 'h3')
    print data
    for s in resultList:
        pageUrl = re.compile(r'http://auction.artron.net/paimai-art\d+/').search(s).group()
        urlList.append(pageUrl)
        print pageUrl

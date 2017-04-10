import requests
from bs4 import BeautifulSoup

class ArtWorkPage:
    def __init__(self, url):
        self.url = url

    def get_info(self):
        try:
            data = requests.get(self.url).content
        except requests.exceptions, e:
            print 'Error: ', e
            return
        soup = BeautifulSoup(data)

        info = {
            'title': soup.body.find('div',{'class':'titLeft'}).h1.text,
            'authors': map(lambda t: t.text.split()[0],soup.body.find('div',{'class':'worksInfo'},id='').table.td.find_all('a'))
            'size':
        }


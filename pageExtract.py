import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


def get_info_by_page(url):
    """This function is to get the basic info from the url provided. """
    headers = {
        'Cookie':'gr_user_id=846d849d-96db-4525-8ae9-c48c1f3fe4cd; tulu_pop=1; PHPSESSID=losun7v447o6hga8kevgndsoq3; _at_pt_0_=2265228; _at_pt_1_=dzl199401; _at_pt_2_=b6e45aeeb11f908546b0378897fb6b81; artron_67ae_saltkey=k5C1F0dH; artron_67ae_lastvisit=1492009218; artron_67ae_sid=YaM0vp; artron_67ae_lastact=1492012818%09uc.php%09; artron_67ae_auth=1887uS6yy%2FNd4XpDdZyC466kWXxsC6C%2BwBxso4oZfLJ2aABH4EgWMEGWEceyMYI2O12Nd27GXMdQBxv4a9NC8drbqpPL; gr_session_id_276fdc71b3c353173f111df9361be1bb=082b1942-f46f-4568-b8c1-3823fbe6a7b9; Hm_lvt_851619594aa1d1fb8c108cde832cc127=1491779761,1491799064,1492011702; Hm_lpvt_851619594aa1d1fb8c108cde832cc127=1492012822'
    }
    data = requests.get(url, headers=headers).content
    soup = BeautifulSoup(data, 'lxml')
    itemName = map(lambda t: t.text.strip(), soup.find('div', {'class': 'worksInfo'}, id='').find_all('th'))
    itemValue = map(lambda t: t.text.strip(), soup.find('div', {'class': 'worksInfo'}, id='').find_all('td'))
    data_line = dict((itemName, itemValue)for itemName, itemValue in zip(itemName, itemValue))
    data_line['url'] = url
    data_line['img_url'] = soup.body.find('img')['src']
    return data_line


def set_info(a):
    if a['isGot']:
        return
    a_new = a
    url = a['url']
    info = get_info_by_page(url)
    a_new['isGot'] = True
    a_new.update(info)
    print aic.replace_one({'_id': a['_id']}, a_new)
    print info

# start client connection
client = MongoClient('localhost', 27017)
# get the info of the database
db = client.art_work_database
aic = db.art_work_collection
print aic.count()
a = aic.find_one()
print a
set_info(a)
print aic.find_one()
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.art_work_database
aic = db.art_work_collection

url_file = open('log.txt', 'r')
for line in url_file:
    aic.insert_one({'url': line[:-2]})

aic.create_index('work_id')
client.close()

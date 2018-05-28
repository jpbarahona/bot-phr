# payload
# https://developers.google.com/hangouts/chat/how-tos/bots-develop

# dnspython or mongodb+srv
# python -m pip install pymongo[srv]
# https://github.com/mongodb/mongo-python-driver/blob/master/doc/installation.rst
import json
import os
import pymongo

pathConfigMongo = './src/mongo/configMongo.json'

config_file = open(pathConfigMongo,'r')
config = json.load(config_file)

client = pymongo.MongoClient(os.environ["MONGO_CONNECTION_STRING_TEST"])

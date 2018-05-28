import src.mongo.connectMongo as cm

# configMongo.json
dbName 		= cm.config["api"]["db"]
collections = cm.config["api"]["hangouts"]["collections"]

# connect/create db
db = cm.client[ dbName ]

# connect/create collection
collMessages = db[ collections["messages"] ]

def guardarMensaje(payload):
	doc_id = collMessages.insert_one(payload).inserted_id
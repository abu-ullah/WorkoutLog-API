from src.services.database import MongoDB

import src.globalvars as globalvars

MongoDBConnection = MongoDB( connectionString= globalvars.CONST_MONGO_URL, dataBaseName= globalvars.CONST_DATABASE)
try:
    MongoDBConnection.connect()
except:
    print("Error connecting to MongoDB Database")
from pymongo import MongoClient, UpdateOne

class MongoDB(object):

    def __init__(self, dataBaseName = None, connectionString = None):
        
        if ((dataBaseName == None) or ( connectionString == None)):
            raise Exception('The Mongo DB dataBaseName and connectionString properties are undefined!')

        self.__dataBaseName = dataBaseName
        self.__connectionString = connectionString
        self.__client = None    
        self.__dataBase = None   

        self.__replicationClient = None   
        self.__replication = False

        self.__lastErrorCode = 0
        self.__lastErrorMessage = ""

    def __del__(self):
        self.disconnect()

    def getLastErrorMessage(self):
        return self.__lastErrorMessage

    @property
    def lastErrorMessage(self):
        self.getLastErrorMessage()
    
    def __setLastError(self, errorCode:int, errorMessage:str = ""):
        self.__lastErrorCode = errorCode
        self.__lastErrorMessage = errorMessage

    @property
    def replication(self):
        return self.__replication

    @property
    def dataBaseName(self):
        return self.__dataBaseName

    def dataBase(self, dataBase = None):
        if (dataBase == None):
            return self.__dataBase
        else:
            self.__dataBase = dataBase

    def client(self, client = None):
        if (client == None):
            return self.__client
        else:
            self.__client = client

    def connect(self) -> bool:
        try:
            self.client(MongoClient(self.__connectionString,  ssl=True))
            dbName = str(self.__dataBaseName)
            self.dataBase(self.client()[dbName])
            return True
        except Exception as e:
            self.__setLastError(1, "Cannot connect to the mongoDB server")
            print(f"(?) MongoDB.connect Exception \n {e}")
            return False

    def disconnect(self) -> bool:
        try:
            self.client().close()
            if self.replication:
                self.__replicationClient.close()
                self.__replication = False
            return True
        except Exception as e:
            self.__setLastError(2, e)
            print(f"(?) MongoDB.disconnect Exception \n {e}")
            return False
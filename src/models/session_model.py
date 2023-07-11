from datetime import datetime, timedelta
import uuid

from src.models.user_model import User
from src.utils.libs import generate_new_session_uuid, generate_encrypted_token

from src.services.__init__ import MongoDBConnection
from src.utils.responses import Responses
import src.globalvars as globalvars

class Session(object):
    
    def __init__(self) -> None:
        self.session_id : uuid = None
        self.date_created : datetime = datetime.now()
        self.expiration_date : datetime = None
        self.loggedUser : User = None
        self.token : str = None
        
    
    ### functions to retrieve, delete sessions
    def get_session(self, session_id):
        try:
            sessionCollection = MongoDBConnection.dataBase(                
                )[globalvars.SESSION_COLLECTION]
            
            session = sessionCollection.find_one({'session_id': session_id})
            
            return session
        except Exception as e:
            raise ValueError('Error finding session:' f'{e}')
        
    ### function to delete expired sessions
    def delete_sessions(self):
        try:
            sessionCollection = MongoDBConnection.dataBase(                
                )[globalvars.SESSION_COLLECTION]
            
            current_datetime = datetime.now()
            
            result = sessionCollection.delete_many({"expiration_date": {"$lt": current_datetime}})
            
            return result
        except Exception as e:
            raise ValueError('Error finding session:' f'{e}')
    
    ## Create a new session when user logs in
    def create_session(self, userFound : User):
        try:
            sessionCollection = MongoDBConnection.dataBase(                
                )[globalvars.SESSION_COLLECTION]
            
            newSession = {
                "session_id": generate_new_session_uuid(),
                "date_created" : datetime.now(),
                "expiration_date": datetime.now() + timedelta(hours=8),
                "loggedUser" : {
                    "user_id" : userFound.user_id,
                    "name" : userFound.name,
                    "email" : userFound.email
                }               
            }
            
            token = generate_encrypted_token(
                newSession['session_id'], 
                newSession['expiration_date'], 
                newSession['loggedUser']['user_id'])

            newSession["token"] = token
                        
            sessionCollection.insert_one(newSession)
            
            #self.delete_sessions()

            return [Responses.SUCCESS, newSession["session_id"], newSession["token"], userFound ]
        except Exception as e:
            raise ValueError('Error logging in:' f'{e}')
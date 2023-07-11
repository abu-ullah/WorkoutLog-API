from datetime import datetime
import uuid, bcrypt

from src.services.__init__ import MongoDBConnection
from src.utils.responses import Responses
import src.globalvars as globalvars

class User(object):
    
    def __init__(self) -> None:
        self.user_id : uuid = None 
        self.password : str = None
        self.email : str = None
        self.name : str = None
        self.date_registered : datetime = datetime.now()

    def toJSON(self):
        return {
            "user_id": self.user_id,
            "name" : self.name,
            "email" : self.email,
            "date_registered": self.date_registered
        }    


    ### functions to retrieve, update, delete users
    def login(self, email, password):
        try:
            userCollection = MongoDBConnection.dataBase(                
            )[globalvars.USER_COLLECTION]
            
            userFound = userCollection.find_one({"email": email})

            if userFound:
                user = User()
                user.user_id = userFound['user_id']
                user.name = userFound['name']
                user.email = userFound['email']
                user.date_registered = userFound['date_registered']
                stored_password = userFound["password"]       
                entered_password = password.encode('utf-8')
                
                if bcrypt.checkpw(entered_password, stored_password):                   
                    return [Responses.SUCCESS, user]
                else:
                    return [Responses.FAIL, "Invalid email or password"]
            else:
                return [Responses.FAIL, "Invalid email or password"]     
        except Exception as e:
            raise ValueError('Error logging in:' f'{e}')
    

    def signup(self):
        try:
            dataBaseConnection = MongoDBConnection.dataBase(                
            )[globalvars.USER_COLLECTION]
            
            # Detect user existed by email
            user_existed = dataBaseConnection.find_one({"email": self.email})
            
            if user_existed:
                return [Responses.FAIL.name, Responses.FAIL.value,"This email was already used!"]

            # Create a new user document
            user_document = {
                "user_id": self.user_id,
                "password": self.password,
                "email": self.email,
                "name": self.name,
                "date_registered": self.date_registered,
                }
            
            # Insert the user document into the database
            dataBaseConnection.insert_one(user_document)

            return [Responses.SUCCESS, self.user_id]
        except Exception as e:
            raise ValueError('Error adding new User:' f'{e}')


    def get_user_info(user_id):
        try:
            
            dataBaseConnection = MongoDBConnection.dataBase(                
            )[globalvars.USER_COLLECTION]
        
            # Detect user existed by email
            user_existed = dataBaseConnection.find_one({"user_id": user_id})

            if user_existed:
                # Create a new user document
                
                user_document = {
                    "email": user_existed['email'],
                    "user_id": user_existed['user_id'],
                    "name": user_existed['name']
                    }
                
                return [Responses.SUCCESS, user_document]
        except Exception as e:
            raise ValueError('Error adding new User:' f'{e}')
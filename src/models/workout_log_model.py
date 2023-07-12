from datetime import datetime
from flask import Response

from src.models.user_model import User

from src.utils.libs import format_date, verify_if_deleted, generate_access_code, pageList, range_by_days, sort_list

from src.services.__init__ import MongoDBConnection
from src.utils.responses import Responses
import src.globalvars as globalvars

import pymongo, uuid

class WorkoutLog(object):
        
    def __init__(self) -> None:
        self.workout_log_id: uuid = None
        self.name : str = None
        self.location : str = None
        self.created_by : User = None
        self.date_added : datetime = None
        self.exercises = []
        self.category : str = None
        self.last_updated : datetime = None
        self.isDeleted : bool = False
    
    def toJSON(self):
        return {
            "workout_log_id": self.workout_log_id,
            "name" : self.name,
            "location" : self.location,
            "created_by" : self.created_by,
            "date_added": self.date_added,
            "exercises": self.exercises,
            "category": self.category,
            "last_updated": self.last_updated,
            "isDeleted" : self.isDeleted
        }
    
    def toJSONList(self):
        JSONList = list()
        for item in self:
            JSONList.append(self.toJSON(item))
        return JSONList
    
    ## Add new workout_log to collection
    def add_workout_log(self):
        try:
            dataBaseConnection = MongoDBConnection.dataBase(                
            )[globalvars.WORKOUT_LOGS_COLLECTION]
            
            new_log = { 
                "workout_log_id": self.workout_log_id,
                "name": self.name,
                "created_by": {
                    "name": self.created_by.name,
                    "email": self.created_by.email,
                    "user_id": self.created_by.user_id
                },
                "location": self.workout_location,
                "exercises": [],
                "date_created": self.date_created,
                "category": self.category,
                "last_updated": self.last_updated,
                "isDeleted" : self.isDeleted   
            }
            result = dataBaseConnection.insert_one(new_log)

            if result is None:
                return [Responses.FAIL, "Error inserting workout_log into collection"]
            else:
                return [Responses.SUCCESS, self.workout_log_id]
                
        except Exception as e:
            raise ValueError('Error adding workout_log to collection:' f'{e}')
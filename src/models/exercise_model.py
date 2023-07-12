from src.services import MongoDBConnection
from src.utils.responses import Responses
import src.globalvars as globalvars

class Exercise(object):
    
    def __init__(self) -> None:
        self.exercise_id : str = None
        self.name : str = None
        self.sets : int = None
        self.reps : float = None
        self.intensity : str = None
        self.notes : str = None

    ## Adds exercise to a workout_log
    def add_exercise(self, workout_log_id, exercise):
        try:
            dataBaseConnection = MongoDBConnection.dataBase(                
            )[globalvars.WORKOUT_LOGS_COLLECTION]
            
            workoutLogFound = dataBaseConnection.find_one({"workout_log_id": workout_log_id})
            
            if not workoutLogFound:
                return [Responses.WORKOUT_LOG_NOT_FOUND, "Workout Log Not Found"]
            
            # Check if exercise already exists in exercises
            for exercise in workoutLogFound.get("exercises", []):
                if exercise["name"] == self.name:
                    return [Responses.FAIL, "You already have a log of this exercise, update that log"]
                
            result = dataBaseConnection.update_one(
                {"workout_log_id": workout_log_id},
                {"$push": {
                    "exercises": {
                        "exercise_id": self.exercise_id,
                        "name": self.name,
                        "sets": self.sets,
                        "reps" : self.reps,
                        "intensity" : self.intensity,
                        "notes" : self.notes
                    }
                }}
            )
        
            return [Responses.SUCCESS, workoutLogFound.get('workout_log_id')]
        except Exception as e:
            raise ValueError('Error adding exercise:' f'{e}')
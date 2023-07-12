from src.models.workout_log_model import WorkoutLog
from src.models.user_model import User

from datetime import datetime
from src.utils.libs import generate_new_workout_log_id, format_date

from src.utils.responses import Responses

def add_log_controller(request_body):
    try:
        logToAdd = WorkoutLog()
        
        logToAdd.workout_log_id = generate_new_workout_log_id()
        logToAdd.date_added = request_body.get('date_added', format_date(datetime.now()))
        logToAdd.name = request_body.get('name')
        logToAdd.location = request_body.get('location', "")
        logToAdd.exercises = request_body.get('exercises', [])
        logToAdd.notes = request_body.get('notes', "")
        logToAdd.last_updated = request_body.get('date_added', format_date(datetime.now()))

        created_by = User()
        created_by.user_id = request_body['created_by'].get('user_id')
        created_by.name = request_body['created_by'].get('name')
        created_by.email = request_body['created_by'].get('email')

        logToAdd.created_by = created_by
        
        response = logToAdd.add_workout_log()
        if response:
            return [Responses.SUCCESS, logToAdd.workout_log_id]
        else:
            return [Responses.FAIL, "Error inserting log into collection"]

    except Exception as e:
        raise Responses.EXCEPTION
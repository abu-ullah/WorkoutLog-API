from datetime import datetime

from src.models.exercise_model import Exercise

from src.utils.libs import generate_new_exercise_id
from src.utils.responses import Responses

def add_exercise_log(request_body):
    try:
        exerciseToAdd = Exercise()
        workout_log_id = request_body.get('workout_log_id', "")
                        
        exerciseToAdd.exercise_id = generate_new_exercise_id()
        exerciseToAdd.name = request_body.get('name')
        exerciseToAdd.sets = request_body.get('sets', 0)
        exerciseToAdd.reps = request_body.get('reps', 0.0)
        exerciseToAdd.intensity = request_body.get('intensity', "")
        exerciseToAdd.notes = request_body.get('notes', "")
        
        response = exerciseToAdd.add_exercise(workout_log_id, exerciseToAdd)
        
        return response
    except Exception as e:
        #LogHandling.exceptionHandling(error= f'{e}', origin= 'SELLOUT_CREATION')
        raise Responses.EXCEPTION
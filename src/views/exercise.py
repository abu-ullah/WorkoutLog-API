from flask import Blueprint, jsonify, request

from src.controllers.exercise_controller import add_exercise_log
from src.middleware.auth import authenticate_session
from src.utils.responses import Responses

exercise_v1 = Blueprint('exercise_v1', __name__)

### Adds participant
@exercise_v1.route('/v1/logs/exercise', methods=['PUT'])
@authenticate_session
def post_exercise_view(self):
    try:
        request_body = request.get_json()
        response = add_exercise_log(request_body)
        
        if response[0] == Responses.WORKOUT_LOG_NOT_FOUND:
            return jsonify({'result': Responses.WORKOUT_LOG_NOT_FOUND.name, 'code': Responses.WORKOUT_LOG_NOT_FOUND.value, "message": response[1]}), 400

        return jsonify({'result': Responses.SUCCESS.name, 'code': Responses.SUCCESS.value, "data": response[1] }), 200
    except Exception as e:
        return jsonify({'code': Responses.EXCEPTION.value}), 500
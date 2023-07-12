from datetime import datetime
from flask import Blueprint, request, jsonify, Response

from src.controllers.workout_log_controller import add_log_controller
from src.middleware.auth import authenticate_session
from src.utils.responses import Responses

workout_log_v1 = Blueprint('workout_log_v1', __name__)

### add a new workout_log
@workout_log_v1.route('/v1/logs/', methods=['POST'])
@authenticate_session
def post_workout_log(self):
    request_body = request.get_json()
    for item in self:
        request_body['created_by'] = item
        exit
    
    response = add_log_controller(request_body)
    
    try: 
        if response[0] == Responses.FAIL:
            return jsonify({'result': Responses.FAIL.name, 'code': Responses.FAIL.value, "message": response[1]}), 400

        if response[0] == Responses.REQUIRED_FIELDS_MISSING:
            return jsonify({'result': Responses.REQUIRED_FIELDS_MISSING.name, 'code': Responses.REQUIRED_FIELDS_MISSING.value, "data": response[1]}), 400

        return jsonify({'result': Responses.SUCCESS.name, 'result_code': Responses.SUCCESS.value, "data": response[1]}), 200
    except Exception as e:
        return jsonify({'code': Responses.EXCEPTION.value}), 500
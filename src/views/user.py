from flask import Blueprint, request, jsonify

from src.controllers.user_controller import add_user, sign_in
from src.utils.responses import Responses

user_v1 = Blueprint('user_v1', __name__)

@user_v1.route('/v1/user/', methods=['POST'])
def create_user():
    try:
        request_body = request.get_json()
        response = add_user(request_body)
        
        if response[0] == Responses.SUCCESS:
            return jsonify({'result': Responses.SUCCESS.name,'result_code':  Responses.SUCCESS.value, 'user_id': response[1] }),200
        else:
            return jsonify({'result': response[0], 'code': response[1], "message": response[2]}), 400
            
    except Exception as e:
        return jsonify({'code': Responses.EXCEPTION.value}), 500
        

@user_v1.route('/v1/user/login', methods=['POST'])
def login():
    try:
        request_body = request.get_json()
        response = sign_in(request_body)
        
        if response[0] == Responses.FAIL:
            return jsonify({'result': Responses.FAIL.name, 'code': Responses.FAIL.value, "message": response[1]}), 400
            
        if response[0] == Responses.REQUIRED_FIELDS_MISSING:
            return jsonify({'result': Responses.REQUIRED_FIELDS_MISSING.name, 'code': Responses.REQUIRED_FIELDS_MISSING.value, "message": response[1]}), 400
        
        return jsonify({'result': Responses.SUCCESS.name,'code':  Responses.SUCCESS.value, 'session_id': response[1], 'token': response[2], 'user': response[3].toJSON() }),200 
    except Exception as e:
        return jsonify({'code': Responses.EXCEPTION.value}), 500
from functools import wraps
from flask import request, jsonify, json
from datetime import datetime
from src.models.user_model import User


from src.utils.libs import decrypt_token

from src.services.__init__ import MongoDBConnection
from src.utils.responses import Responses
import src.globalvars as globalvars
from pymongo import MongoClient

def authenticate_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        token = request.headers.get('Access-Token')

        if token is None:
            return jsonify({'message': 'Access token is missing'}), 401

        try:
            # Decrypt the token
            decoded_token = decrypt_token(token)

            decoded_token_dict = json.loads(decoded_token)

            session_id = decoded_token_dict["session_id"]
            
            sessionCollection = MongoDBConnection.dataBase(                
                )[globalvars.SESSION_COLLECTION]

            
            if not session_id:
                return jsonify({'message': 'Invalid access token'}), 401
            
            # Verify session ID in MongoDB and check if it's expired
            session = sessionCollection.find_one({'session_id': session_id})

            if not session or session.get('expiration_date') < datetime.now():
                return jsonify({'message': 'Invalid or expired session'}), 401
            
            user_info = User.get_user_info(decoded_token_dict['user_id'])
            
        except Exception as e:
            return Responses.EXCEPTION

        # If the session is valid, proceed to the endpoint's function
        result = func(user_info,*args, **kwargs)
        
        return result

    return wrapper

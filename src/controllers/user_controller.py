from datetime import datetime
import json

from src.models.user_model import User
from src.models.session_model import Session
from src.utils.libs import generate_new_user_uuid, generate_hash_password, format_date

from src.utils.responses import Responses
from src.utils.validations import check_digits, check_email, check_length, check_signup_fields, missingFields, validate_password


def add_user(req):
    try:
        userToAdd = User()
        
        # Body Request
        password = req.get("password")
        email = req.get("email")
        name = req.get("name")
        listFields = [password, email, name]
        
        # Validations
        # Check missing fields
        missingFieldsMessage = missingFields(listFields)
        if missingFieldsMessage is not None:
            return missingFieldsMessage
        # Create a dictionary to map the validations
        validation_cases = {

            # Check for empty values
            1: check_signup_fields(req),
            # Validate name field
            2: check_digits(req, 'name'),
            # Validate field length
            3: check_length(req, 'name', 80),
            # Validate email field
            4: check_email(req, 'email', '@'),
            # Check password
            5: validate_password(req,'password',8,12),
        }
        
        # Iterate over each case and execute the corresponding action
        for key, value in validation_cases.items():
            if value is not None:
                return value

        userToAdd.user_id = generate_new_user_uuid()
        hashed_password = generate_hash_password(password=password)
        userToAdd.password = hashed_password
        userToAdd.email = email.lower()
        userToAdd.name = name
        userToAdd.date_registered: datetime = format_date(datetime.now())
        
        response = userToAdd.signup()
        return response
    except Exception as e:
        raise Responses.EXCEPTION
    
    
def sign_in(request_body):
    try:
        user = User()
        email = request_body.get("email").lower()
        password = request_body.get("password")

        if email == "" or password == "":
                return [Responses.REQUIRED_FIELDS_MISSING, "Email or password is missing"]
        
        userAuth = user.login(email=email, password=password)
        if userAuth[0] == Responses.SUCCESS:
            session = Session()
            session_creation = session.create_session(userAuth[1])
        else:
            return userAuth

        return session_creation
    except Exception as e:
        raise Responses.EXCEPTION     



import json
import re

from src.utils.responses import Responses

def missingFields(fieldList):
        print(fieldList)
    # Iterate over each case and execute the corresponding action
        for itemField in fieldList:
            if itemField is None:
                return [Responses.REQUIRED_FIELDS_MISSING.name, Responses.REQUIRED_FIELDS_MISSING.value,"Required Field(s) Missing"]
            
        return None

def check_signup_fields(fieldsList):
    # Check for empty values
    for key, value in fieldsList.items():
        if not value:
            return [Responses.REQUIRED_FIELDS_EMPTY.name, Responses.REQUIRED_FIELDS_EMPTY.value, f"The field '{key}' has an empty value."]
        if value.isspace():
            return [Responses.REQUIRED_FIELDS_EMPTY.name, Responses.REQUIRED_FIELDS_EMPTY.value, f"The field '{key}' has only spaces value."]
        
    return None

def check_digits(fieldList, fieldToCheck):
    # Validate the field
    field = fieldList.get(fieldToCheck, "")

    if re.search(r'\d', field):
        return [Responses.NUMBERS_NOT_ALLOWED.name, Responses.NUMBERS_NOT_ALLOWED.value, f"The field '{fieldToCheck}' must not contain numbers."]
    else:
        return None
    
def check_length(fieldList, fieldToCheck,lengthToCheck):
    # Validate the field
    field = fieldList.get(fieldToCheck, "")

    if len(field) > lengthToCheck:
        return [Responses.LENGTH_NOT_ALLOWED.name, Responses.LENGTH_NOT_ALLOWED.value, f"The field '{fieldToCheck}' should be maximum {lengthToCheck} characters."]
    else:
        return None
    
def check_email(fiedToCheck, field, symbol):
    # Validate the email field
    email = fiedToCheck.get(field, "")

    if "@" not in email:
        return [Responses.INVALID_EMAIL.name, Responses.INVALID_EMAIL.value, f"The {field} field should contain the {symbol} symbol."]
    elif re.search(r'\s', email):
        return [Responses.INVALID_EMAIL.name, Responses.INVALID_EMAIL.value,f"The {field} field should be one word (no whitespace)."]
    else:
        return None
    

def validate_password(fiedToCheck,field,min_length,max_length):
    # Validate the email field
    password = fiedToCheck.get(field, "")
    # Minimum length: 8 symbols
    if len(password) < min_length:
        return [Responses.LENGTH_NOT_ALLOWED.name, Responses.LENGTH_NOT_ALLOWED.value, f"The field '{field}' should be minimun {min_length} characters."]


    # Maximum length: 12 symbols
    if len(password) > 12:
        return [Responses.LENGTH_NOT_ALLOWED.name, Responses.LENGTH_NOT_ALLOWED.value, f"The field '{field}' should be maximun {max_length} characters."]


    # At least 1 uppercase letter
    if not re.search(r'[A-Z]', password):
        return [Responses.INVALID_PASSWORD.name, Responses.INVALID_PASSWORD.value, f"The field '{field}' must contain at least one uppercase letter"]


    # At least 1 lowercase letter
    if not re.search(r'[a-z]', password):
        return [Responses.INVALID_PASSWORD.name, Responses.INVALID_PASSWORD.value, f"The field '{field}' must contain at least one lowercase letter"]

    # At least 1 digit
    if not re.search(r'\d', password):
        return [Responses.INVALID_PASSWORD.name, Responses.INVALID_PASSWORD.value, f"The field '{field}' must contain at least one digit"]


    # All criteria are met
    return None
import uuid, datetime, bcrypt
import secrets, os, string

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

from src.utils.responses import Responses

def generate_new_workout_log_id() -> str :
  workoutLogId = str(uuid.uuid4().hex)

  return workoutLogId


def generate_new_user_uuid() -> str :
  userId = str(uuid.uuid4().hex)

  return userId


def generate_new_session_uuid() -> str :
  sessionId = str(uuid.uuid4().hex)

  return sessionId

def generate_new_exercise_id() -> str :
  exerciseId = str(uuid.uuid4().hex)

  return exerciseId


def generate_hash_password(password) -> str:
  salt = bcrypt.gensalt()
  hashedPassword = bcrypt.hashpw(password.encode("utf-8"), salt )

  return hashedPassword


def verify_password(entered_password, stored_hashed_password):
    return bcrypt.checkpw(entered_password.encode("utf-8"), stored_hashed_password.encode("utf-8"))

  
def generate_encrypted_token(session_id, expiration_date, user_id):
    # Encode the session_id, expiration_date, and user_id as a JSON string
    json_data = f'{{"session_id": "{session_id}", "user_id": "{user_id}", "expiration_date": "{expiration_date}"}}'

    # Convert the secret key to bytes
    secret_key = os.getenv("SECRET_KEY").encode()

    cipher = AES.new(secret_key, AES.MODE_CBC)

    padded_data = pad(json_data.encode(), AES.block_size)

    encrypted_data = cipher.encrypt(padded_data)
    iv_and_encrypted_data = cipher.iv + encrypted_data

    # Base64 encode the IV and encrypted data
    encoded_token = b64encode(iv_and_encrypted_data).decode()

    return encoded_token  
  
def decrypt_token(encoded_token):
    # Convert the secret key to bytes
    secret_key = os.getenv("SECRET_KEY").encode()

    # Base64 decode the encoded token
    iv_and_encrypted_data = b64decode(encoded_token)

    iv = iv_and_encrypted_data[:AES.block_size]

    encrypted_data = iv_and_encrypted_data[AES.block_size:]

    cipher = AES.new(secret_key, AES.MODE_CBC, iv)

    decrypted_data = cipher.decrypt(encrypted_data)
    
    unpadded_data = unpad(decrypted_data, AES.block_size)

    # Convert the JSON string to a dictionary
    token_data = unpadded_data.decode()
    
    return token_data  
  
def generate_access_code():
  characters = string.ascii_letters + string.digits
  access_code = ''.join(secrets.choice(characters) for i in range(8))
  return access_code

def format_date(date):
    formatted_date = date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return formatted_date
  
def isodate_to_datetime(iso_date):
  date_only = dateutil.parser.isoparse(iso_date).date()
  return date_only
  
### Used to get list of inventories
def sort_list(modelList, fieldToSort):
  ## Sort the inventory list by the soonest due_date and the name field by alphabetical order
  return sorted(modelList, key=lambda x: (x[fieldToSort]))

def pageList(modelList, page):
  start_index = (page - 1) * Responses.NUMBER_OF_PAGES.value  # Number of documents to skip based on the page number
  modelList = modelList[start_index:int(start_index + Responses.NUMBER_OF_PAGES.value)]
  return modelList

def range_by_days(modelList, days, toDate):
  today = isodate_to_datetime(toDate)
  if toDate is None:
    today = format_date(datetime.date.today())
    past_date = format_date(today - datetime.timedelta(days))
  else:
    past_date = today - datetime.timedelta(days)
    
  filtered_inventories = []

  for inventory in modelList:
      last_updated = isodate_to_datetime(inventory["last_updated"][:-1])
      
      if past_date < last_updated <= today:
          filtered_inventories.append(inventory)

  return filtered_inventories

def verify_if_deleted(isDeleted):
    if isDeleted == True:
      return False
    else:
      return True

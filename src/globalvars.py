import os

from dotenv.main import load_dotenv
import os

load_dotenv()

'''DATABASE'''
CONST_MONGO_URL = os.environ.get('CONST_MONGO_URL')
CONST_DATABASE = os.environ.get('CONST_DATABASE')

'''COLLECTIONS'''
WORKOUT_LOGS_COLLECTION = os.getenv('WORKOUT_LOGS_COLLECTION')
USER_COLLECTION = os.getenv('USER_COLLECTION')
SESSION_COLLECTION = os.getenv('SESSION_COLLECTION')
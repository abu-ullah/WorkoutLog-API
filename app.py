from flask import Flask, render_template, jsonify, request, Blueprint
import src.globalvars as globalvars
from flask_cors import CORS

from src.views.user import user_v1
from src.views.workout_log import workout_log_v1
from src.views.exercise import exercise_v1
from src.utils.responses import Responses

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.register_blueprint(user_v1)
app.register_blueprint(workout_log_v1)
app.register_blueprint(exercise_v1)

CORS(app, supports_credentials= True)

@app.route("/")
def index():
    return ""

@app.errorhandler(404)
def errorHandle_404(self):
    return "error 404"

@app.errorhandler(500)
def errorHandle_500(self):
    return "error 500"

if __name__ == "__main__":
    app.run()
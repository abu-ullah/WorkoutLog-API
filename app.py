from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CORS(app, supports_credentials= True)

@app.route("/")
def index():
    return "Product Catalog"

@app.errorhandler(404)
def errorHandle_404(self):
    return "error 404"

@app.errorhandler(500)
def errorHandle_500(self):
    return "error 500"

if __name__ == "__main__":
    app.run()
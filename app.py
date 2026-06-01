from flask import Flask, render_template
from flask_cors import CORS
from routes.Prediction import prediction_bp
from routes.utils.validators import validate_patient
app = Flask(__name__)
CORS(app)

app.register_blueprint(prediction_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
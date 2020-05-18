from flask import Flask, render_template, request, jsonify
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    global data_us
    
    return render_template("index.html")


if __name__ == "__main__":
    data_us = pd.read_csv('data/us-states-latest.csv')
    app.run(debug=True)

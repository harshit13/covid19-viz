from flask import Flask, render_template, request, jsonify
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

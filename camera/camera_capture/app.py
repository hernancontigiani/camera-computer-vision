import traceback
import json

from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)
app.secret_key = 'ptSecret'
app.config['SECRET_KEY'] = 'ptSecret'


# ---- Endpoints ----
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5021)

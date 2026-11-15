from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return "<h3>Welcome to the Flask API!</h3>"


if __name__ == "__main__":
    app.run(debug=True)
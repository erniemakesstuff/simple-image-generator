from flask import Flask

app = Flask(__name__)

@app.route("/health")
def health_check():
    return "Healthy"

@app.route("/image")
def create_image():
    return "TODO"
from flask import Flask, request
import lexica_client
import threading

app = Flask(__name__)

@app.route("/health")
def health_check():
    return "Healthy"


# Accept json body
# promptInstruction: string
# contentLookupKey: string
@app.route("/image", methods=["POST"])
def create_image():
    data = request.get_json()  # Get the JSON data from the request
    def query_and_store():
        lexica_client.get_image(data["promptInstruction"], data["contentLookupKey"], data["filepathPrefix"])
    t1 = threading.Thread(target=query_and_store)
    t1.start()
    return "Ok"
from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread
from workers.workers import translation_worker
import requests

app = Flask(__name__)
CORS(app)
	
@app.route("/", methods=["GET"])
def hello():
    return "We are live Houston!"

@app.route("/translate", methods=["GET"])
def translate():
    Thread(target = start_translate).start()
    return jsonify(action="success")

def start_translate():
    data = requests.get('https://searchori.net/articles/translate')
    iran = []

    for article in data.json()['data']:
        if article['country'] == 'iran':
            iran.append(article)

    if len(iran) != 0:
        Thread(target = translation_worker, args=(iran, 'fa',)).start()

if __name__ == '__main__':
    app.debug = True
    app.run()
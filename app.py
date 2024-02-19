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

@app.route("/danish", methods=["POST"])
def danish():
    news = request.json.get('data')
    Thread(target = translation_worker, args=(news, 'da',)).start()
    return jsonify(action="success")


@app.route("/swedish", methods=["POST"])
def swedish():
    news = request.json.get('data')
    Thread(target = translation_worker, args=(news, 'sv',)).start()
    return jsonify(action="success")

@app.route("/norwegian", methods=["POST"])
def norwegian():
    news = request.json.get('data')
    Thread(target = translation_worker, args=(news, 'no',)).start()
    return jsonify(action="success")

@app.route("/translate", methods=["GET"])
def translate():
    Thread(target = start_translate).start()
    return jsonify(action="success")

def start_translate():
    data = requests.get('https://searchori.net/articles/translate')
    denmark = []
    sweden = []
    norway = []
    print('json!!!', data['data'].json())
    print('not json!!!', data['data'])
    
    for article in data['data'].json():
        if article['country'] == 'denmark':
           denmark.append(article)
        elif article['lang'] == 'sweden':
            sweden.append(article)
        elif article['lang'] == 'norway':
            norway.append(article)
    
    Thread(target = translation_worker, args=(denmark, 'da',)).start()
    Thread(target = translation_worker, args=(sweden, 'sv',)).start()
    Thread(target = translation_worker, args=(norway, 'no',)).start()


if __name__ == '__main__':
    app.debug = True
    app.run()
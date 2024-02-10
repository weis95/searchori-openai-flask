from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread
from workers.workers import translation_worker

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

if __name__ == '__main__':
    app.debug = True
    app.run()
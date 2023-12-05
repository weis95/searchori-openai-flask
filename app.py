from openai import OpenAI
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
	
@app.route("/", methods=["GET"])
def hello():
    return "Hello World!"

@app.route("/", methods=["POST"])
def summarize():
    user = os.environ.get('OPENAI')
    client = OpenAI(
        api_key=user,
    )

    data = request.json.get('data')
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": f"Write a summary of this text: {data}"},
        ],
    )

    # print(response.choices[0].message.content)
    return jsonify(summary=response.choices[0].message.content)


if __name__ == '__main__':
    app.debug = True
    app.run()
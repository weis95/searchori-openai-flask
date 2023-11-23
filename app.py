from openai import OpenAI
from flask import Flask, jsonify, request

app = Flask(__name__)
	
@app.route("/", methods=["GET"])
def hello():
    return "Hello World!"

@app.route("/", methods=["POST"])
def summarize():
    client = OpenAI(
        api_key="sk-<your-key>",
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
from flask import Flask, jsonify, render_template, request
import json
from datetime import datetime

app = Flask(__name__)
with open('daily.json', 'rb') as f:
	data = f.readlines()

data = json.loads(data[0])
lst = []
for key, value in data.items():
	lst.append([key.replace("-", ","), value])

@app.route('/_add_numbers')
def add_numbers():
	"""Add two numbers server side, ridiculous but well..."""
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	return jsonify(result=a + b)


@app.route('/')
def index():
	return render_template('index.html', lst = lst)

if __name__ == "__main__":
	app.run()

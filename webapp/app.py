from flask import Flask, jsonify, render_template, request
from datetime import datetime, date, timedelta
# import calendar
import json

app = Flask(__name__)
with open('daily.json', 'rb') as f:
	data = f.readlines()

data = json.loads(data[0])
lst = []
for key, value in data.items():
	lst.append([key.replace("-", ","), value])

@app.route('/_get_data')
def get_data():
	"""Add two numbers server side, ridiculous but well..."""
	year_month = request.args.get('a', type=str)
	year_month = year_month.split('-')
	year = int(year_month[0])
	month = int(year_month[1])
	tmp = month
	# my_cal = calendar.Calendar()
	first = date(year, month, 1)
	m_lst = []
	while  month <  tmp + 1:
		m_lst += [first]
		first += timedelta(days=1)
		month = first.month
	# for i in my_cal().monthdatescalendar(int(my_cal[0]), int(my_cal[1])):
	# 	m_lst += map(lambda x: str(x), i)
	m_lst = sorted(map(lambda x: str(x), m_lst))
	return jsonify(result=m_lst)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/calendar')
def calendar():
	return render_template('calendar.html', lst = lst)

@app.route('/heatmap')
def heatmap():
	return render_template('heatmap.html', lst = lst)

@app.route('/prediction')
def prediction():
	return render_template('prediction.html')

if __name__ == "__main__":
	app.run(debug=True)

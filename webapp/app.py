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

with open('hourly.json', 'rb') as f:
	h_data = f.readlines()

h_data = json.loads(h_data[0])

@app.route('/_get_data')
def get_data():
	"""Add two numbers server side, ridiculous but well..."""
	year_month = request.args.get('a', type=str)
	year_month = year_month.split('-')
	year = int(year_month[0])
	month = int(year_month[1])
	tmp_m = month
	tmp_y = year
	# my_cal = calendar.Calendar()
	first = date(year, month, 1)
	m_lst = []
	while  month <  tmp_m + 1 and year < tmp_y + 1:
		m_lst += [first]
		first += timedelta(days=1)
		month = first.month
		year = first.year
	# for i in my_cal().monthdatescalendar(int(my_cal[0]), int(my_cal[1])):
	# 	m_lst += map(lambda x: str(x), i)
	m_lst = sorted(map(lambda x: str(x), m_lst))
	n = len(m_lst)
	y = range(24)
	t = []
	for i in range(24):
		t += [map(lambda x: [x], range(n))]
	tt = []
	for j in range(n):
		tt += [map(lambda x: t[x][j] + [x], range(24))]
	ttt = []
	for k in range(n):
		ttt += map(lambda x, y: x + [y], tt[k], h_data[m_lst[k]])
	return jsonify(day_lst=m_lst, data_lst=ttt, y=y)


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

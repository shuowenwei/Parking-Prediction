import os
from flask import Flask, render_template, jsonify, redirect, url_for, request, flash
from datetime import datetime, date, timedelta
from sklearn.metrics import r2_score, mean_squared_error
# import calendar
import json
import csv

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
# ALLOWED_EXTENSIONS = ['csv']

with open('daily.json', 'rb') as f:
	data = f.readlines()

data = json.loads(data[0])
lst = []
for key, value in data.items():
	lst.append([key.replace("-", ","), value])

with open('hourly.json', 'rb') as f:
	h_data = f.readlines()

h_data = json.loads(h_data[0])

with open('201601.json', 'rb') as f:
	jan16_data = f.readlines()

jan16_data = json.loads(jan16_data[0])

with open('201602.json', 'rb') as f:
	feb16_data = f.readlines()

feb16_data = json.loads(feb16_data[0])

r2_jan16 = r2_score(jan16_data['y_true'], jan16_data['y_pred'])

@app.route('/_get_h_data')
def get_h_data():
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

@app.route('/_get_d_data')
def get_d_data():
	"""Add two numbers server side, ridiculous but well..."""
	start_date = datetime.strptime((request.args.get('a', type=str)), '%Y-%m-%d').date()
	end_date = datetime.strptime((request.args.get('b', type=str)), '%Y-%m-%d').date()
	dict = {}
	while start_date < end_date:
		dict[str(start_date)] = h_data[str(start_date)]
		start_date += timedelta(days=1)
	dict[str(end_date)] = h_data[str(end_date)]
	return jsonify(dict=dict)

actual_lst = []
r2_feb16 = 0
if len(actual_lst) == len(feb16_data['y_pred']):
	r2_feb16 = r2_score(actual_lst, feb16_data['y_pred'])
@app.route('/upload', methods=['POST'])
def upload():
	if request.method == 'POST':
		f = request.files['file_source']
		print "===================================="
		if not f:
			return redirect(url_for('prediction'))
		now = datetime.now()
		filename = os.path.join(app.config['UPLOAD_FOLDER'], "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), f.filename.rsplit('.', 1)[1]))
		f.save(filename)
		tmp_actual_lst = []
		with open(filename, 'rb') as csvfile:
			csvreader = csv.DictReader(csvfile)
			for i in csvreader:
				tmp_actual_lst += [int(i['occupancy'])]
		global actual_lst
		actual_lst = tmp_actual_lst
		return render_template('prediction.html', 
			jan16_data=jan16_data, feb16_data=feb16_data,
			tmp_actual_lst=tmp_actual_lst, actual_lst=actual_lst, 
			r2_jan16=r2_jan16, r2_feb16=r2_feb16)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/calendar')
def calendar():
	return render_template('calendar.html', lst=lst)

@app.route('/heatmap')
def heatmap():
	return render_template('heatmap.html')

@app.route('/linechart')
def linechart():
	return render_template('linechart.html')

@app.route('/prediction')
def prediction():
	return render_template('prediction.html',
		jan16_data=jan16_data, feb16_data=feb16_data, actual_lst=actual_lst,
		r2_jan16=r2_jan16, r2_feb16=r2_feb16)

if __name__ == "__main__":
	# app.secret_key = 'super secret key'
	# app.config['SESSION_TYPE'] = 'filesystem'
	app.run(debug=True)

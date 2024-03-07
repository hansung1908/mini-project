from flask import Flask, redirect, url_for, request, render_template

import weather

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    location = request.form['location']
    return redirect(url_for('view', location=location))

@app.route("/view")
def view():
    location = request.args.get('location')
    weather_info = weather.weather_data.get(location, "날씨 정보를 찾을 수 없습니다.")
    return render_template('view.html', location=location, weather_info=weather_info)


app.run(debug=True)
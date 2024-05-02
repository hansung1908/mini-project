from flask import Flask, redirect, url_for, request, render_template
from datetime import datetime

import weather
import demo.capstone_demo
import old_weather

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/select")
def select():
    return render_template('select.html')


@app.route('/submit', methods=['POST'])
def submit():
    location = request.form['location']
    date = request.form['date']
    return redirect(url_for('view', date=date, location=location))


@app.route("/view")
def view():
    location = request.args.get('location')
    date = request.args.get('date')

    today = datetime.now().date()
    input_datetime = datetime.strptime(date, '%Y-%m-%d').date()

    if input_datetime == today:
        weather_info = weather.weather_data.get(location, "날씨 정보를 찾을 수 없습니다.")
        style_tag = demo.capstone_demo.ai(weather_info['기온'], weather_info['강수량'])
        return render_template('view.html', location=location, weather_info=weather_info, style_tag=style_tag)

    else:
        weather_info = old_weather.get(date, location)
        style_tag = demo.capstone_demo.ai(weather_info['기온'], weather_info['강수량'])
        return render_template('view.html', location=location, weather_info=weather_info, style_tag=style_tag)


app.run(debug=True)
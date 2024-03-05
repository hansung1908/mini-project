from flask import Flask, redirect, url_for, request, render_template

import weather

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    location = request.form['location']
    return redirect(url_for('view', location = location))

@app.route("/view")
def view():
    location = request.args.get('location')
    weather_info = weather.weather_data.get(location, "날씨 정보를 찾을 수 없습니다.")
    return f"지역: {location}<br>기온: {weather_info['기온']}℃<br>강수량: {weather_info['강수량']}mm<br>풍속: {weather_info['풍속']}m/s"


app.run(debug=True)
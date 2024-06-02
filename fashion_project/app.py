import now_weather
import old_weather
import image_date
import style_model.style_pred_model
import length_model.length_pred_model

from flask import Flask, redirect, url_for, request, render_template
from datetime import datetime

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
    gender = request.form['gender']
    return redirect(url_for('view', date=date, location=location, gender=gender))


@app.route("/view")
def view():
    location = request.args.get('location')
    date = request.args.get('date')
    gender = request.args.get('gender')

    today = datetime.now().date()
    input_datetime = datetime.strptime(date, '%Y-%m-%d').date()

    random_images, images_and_dates = image_date.get_random_image_and_date(gender)

    if input_datetime == today:
        weather_info = now_weather.weather_data.get(location, "날씨 정보를 찾을 수 없습니다.")
        style_tag = style_model.style_pred_model.play(weather_info['기온'], weather_info['강수량'])
        length_tag = length_model.length_pred_model.play(weather_info['기온'])
        return render_template('view.html', images_and_dates=images_and_dates, random_images=random_images,
                               date=today, location=location, weather_info=weather_info, style_tag=style_tag,
                               length_tag=length_tag, gender=gender)

    else:
        weather_info = old_weather.get(date, location)
        style_tag = style_model.style_pred_model.play(weather_info['기온'], weather_info['강수량'])
        length_tag = length_model.length_pred_model.play(weather_info['기온'])
        return render_template('view.html', images_and_dates=images_and_dates, random_images=random_images,
                               date=date, location=location, weather_info=weather_info, style_tag=style_tag,
                               length_tag=length_tag, gender=gender)


app.run(debug=True)

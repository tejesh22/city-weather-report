from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != "404":
        # Extract relevant weather information
        temperature = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Return weather information
        return {
            "city": city,
            "temperature": temperature,
            "weather_desc": weather_desc,
            "humidity": humidity,
            "wind_speed": wind_speed
        }
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city_name = request.form['city']
        weather_data = get_weather(API_KEY, city_name)

        if weather_data:
            return render_template('weather.html', weather=weather_data)
        else:
            error_msg = "City not found."
            return render_template('index.html', error=error_msg)
    else:
        return render_template('index.html')

# Enter your OpenWeatherMap API key here
API_KEY = "397130a7ebe353979ece21b5f22d551b"

if __name__ == '__main__':
    app.run(debug=True)

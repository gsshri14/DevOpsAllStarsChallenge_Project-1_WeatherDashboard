import os
from flask import Flask, request, render_template, redirect, url_for, flash
from dotenv import load_dotenv
from WeatherDashboard import WeatherDashboard

# Load environment variables from a .env file (optional, for local development)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Securely set the secret key

dashboard = WeatherDashboard()
dashboard.create_bucket_if_not_exists()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_weather', methods=['POST'])
def fetch_weather():
    city = request.form['city']
    if not city:
        flash('Please enter a city name', 'error')
        return redirect(url_for('index'))

    weather_data = dashboard.fetch_weather(city)
    if weather_data:
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']

        weather_info = {
            'city': city,
            'temp': temp,
            'feels_like': feels_like,
            'humidity': humidity,
            'description': description
        }

        # Save to S3
        success = dashboard.save_to_s3(weather_data, city)
        if success:
            flash(f'Weather data for {city} saved to S3!', 'success')
        else:
            flash(f'Failed to save weather data for {city}', 'error')

        return render_template('index.html', weather_info=weather_info)
    else:
        flash(f'Failed to fetch weather data for {city}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
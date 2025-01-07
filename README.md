# Weather Dashboard

## Overview

The Weather Dashboard is a Python application that fetches weather data from the OpenWeather API and saves it to an AWS S3 bucket. The application is designed to be run as a script, fetching weather data for a list of cities and storing the data in a structured format in S3.

## Features

- Fetches current weather data for specified cities from the OpenWeather API.
- Saves the fetched weather data to an AWS S3 bucket.
- Automatically creates the S3 bucket if it does not exist.

## Requirements

- Python 3.6+
- `boto3` library for interacting with AWS S3.
- `requests` library for making HTTP requests.
- `python-dotenv` library for loading environment variables from a `.env` file.

## Project Structure
- `src/main/WeatherDashboard.py`: Main application code.
- `src/test/TestWeatherDashboard.py`: Unit tests for the application.
- `README.md`: Project documentation.
- `requirements.txt`: List of dependencies.
- `.env`: Environment variables file (not included in the repository to avoid exposure to sensitive data).

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/saacertificate1403/weather-dashboard.git
    cd weather-dashboard
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory of the project and add your OpenWeather API key and AWS S3 bucket name:
    ```env
    OPENWEATHER_API_KEY=your_openweather_api_key
    AWS_BUCKET_NAME=your_s3_bucket_name
    ```

## Usage

1. Run the main script to fetch weather data for the specified cities and save it to the S3 bucket:
    ```sh
    python src/main/WeatherDashboard.py
    ```

2. To run the unit tests, use the following command:
    ```sh
    python -m unittest discover -s src/test
    ```
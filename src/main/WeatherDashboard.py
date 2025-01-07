import os
import json
import boto3
import requests
from datetime import datetime
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class WeatherDashboard:
    """
    A class to represent a weather dashboard that fetches weather data from the OpenWeather API
    and saves it to an AWS S3 bucket.
    """

    def __init__(self):
        """
        Initializes the WeatherDashboard with API key and S3 bucket name from environment variables.
        Also initializes the S3 client.
        """
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client('s3')

    def create_bucket_if_not_exists(self):
        """
        Creates an S3 bucket if it does not already exist.
        """
        try:
            # Check if the bucket exists
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except ClientError as e:
            # If head_bucket throws a ClientError, it means the bucket doesn't exist
            error_code = e.response['Error']['Code']
            if error_code == '404':
                try:
                    # Only create the bucket if it doesn't exist
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                    print(f"Successfully created bucket {self.bucket_name}")
                except Exception as e:
                    print(f"Error creating bucket: {e}")
            else:
                # Handle other potential errors that are not related to the bucket not existing
                print(f"Error checking bucket: {e}")

    def fetch_weather(self, city):
        """
        Fetches weather data from the OpenWeather API for a given city.

        Parameters:
        city (str): The name of the city to fetch weather data for.

        Returns:
        dict: The weather data for the city, or None if an error occurs.
        """
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def save_to_s3(self, weather_data, city):
        """
        Saves weather data to an S3 bucket.

        Parameters:
        weather_data (dict): The weather data to save.
        city (str): The name of the city the weather data is for.

        Returns:
        bool: True if the data was successfully saved, False otherwise.
        """
        if not weather_data:
            return False

        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"

        try:
            weather_data['timestamp'] = timestamp
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfully saved data for {city} to S3")
            return True
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False
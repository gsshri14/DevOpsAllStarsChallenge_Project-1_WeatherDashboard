import unittest
from unittest.mock import patch, MagicMock
import requests
from src.main.WeatherDashboard import WeatherDashboard
from botocore.exceptions import ClientError

class TestWeatherDashboard(unittest.TestCase):
    """
    Unit tests for the WeatherDashboard class.
    """

    @patch('src.main.WeatherDashboard.boto3.client')
    @patch('src.main.WeatherDashboard.os.getenv')
    def setUp(self, mock_getenv, mock_boto3_client):
        """
        Sets up the test environment by mocking environment variables and the S3 client.
        """
        mock_getenv.side_effect = lambda key: {
            'OPENWEATHER_API_KEY': 'fake_api_key',
            'AWS_BUCKET_NAME': 'fake_bucket_name'
        }[key]
        self.mock_s3_client = MagicMock()
        mock_boto3_client.return_value = self.mock_s3_client
        self.dashboard = WeatherDashboard()

    @patch('src.main.WeatherDashboard.requests.get')
    def test_fetches_weather_data_successfully(self, mock_get):
        """
        Tests that weather data is fetched successfully from the OpenWeather API.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {'main': {'temp': 70, 'feels_like': 68, 'humidity': 50}, 'weather': [{'description': 'clear sky'}]}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = self.dashboard.fetch_weather('Philadelphia')
        self.assertIsNotNone(result)
        self.assertEqual(result['main']['temp'], 70)

    @patch('src.main.WeatherDashboard.requests.get')
    def test_handles_weather_data_fetch_failure(self, mock_get):
        """
        Tests that the fetch_weather method handles API request failures gracefully.
        """
        mock_get.side_effect = requests.exceptions.RequestException("API failure")
        result = self.dashboard.fetch_weather('Philadelphia')
        self.assertIsNone(result)

    def test_creates_bucket_if_not_exists(self):
        """
        Tests that the S3 bucket is created if it does not already exist.
        """
        # Simulate ClientError with a 404 error code (bucket not found)
        self.mock_s3_client.head_bucket.side_effect = ClientError(
            error_response={'Error': {'Code': '404', 'Message': 'Not Found'}},
            operation_name='HeadBucket'
        )
        self.dashboard.create_bucket_if_not_exists()
        self.mock_s3_client.create_bucket.assert_called_once_with(Bucket='fake_bucket_name')

    def test_does_not_create_bucket_if_exists(self):
        """
        Tests that the S3 bucket is not created if it already exists.
        """
        self.mock_s3_client.head_bucket.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}  # Simulate bucket exists
        self.dashboard.create_bucket_if_not_exists()
        self.mock_s3_client.create_bucket.assert_not_called()

    def test_saves_weather_data_to_s3_successfully(self):
        """
        Tests that weather data is saved to the S3 bucket successfully.
        """
        weather_data = {'main': {'temp': 70, 'feels_like': 68, 'humidity': 50}, 'weather': [{'description': 'clear sky'}]}
        result = self.dashboard.save_to_s3(weather_data, 'Philadelphia')
        self.assertTrue(result)
        self.mock_s3_client.put_object.assert_called_once()

    def test_handles_s3_save_failure(self):
        """
        Tests that the save_to_s3 method handles S3 save failures gracefully.
        """
        self.mock_s3_client.put_object.side_effect = Exception("S3 failure")
        weather_data = {'main': {'temp': 70, 'feels_like': 68, 'humidity': 50}, 'weather': [{'description': 'clear sky'}]}
        result = self.dashboard.save_to_s3(weather_data, 'Philadelphia')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
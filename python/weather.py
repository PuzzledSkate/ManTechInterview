#!/usr/bin/python
import argparse
import os
import sys
from typing import Tuple

import requests


API_KEY = os.getenv('OW_API')

class Weather:

  def __init__(self, args) -> None:
      self.args = args
      self.api_key = API_KEY
      self.session = self._session()

  def _session(self) -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session

  def _get(self, url: str) -> requests.Response:
        response = self.session.get(url)
        response.raise_for_status()
        return response

  def _get_coord(self) -> Tuple[str,str]:
      latitude = ""
      longitude = ""
      coordinates_url= f"http://api.openweathermap.org/geo/1.0/zip?zip={self.args.zip},{self.args.country}&appid={self.api_key}"

      response = self._get(coordinates_url)
      coordinates = response.json()
      
      #print(coordinates)
      latitude = coordinates['lat']
      longitude = coordinates['lon']

      return latitude, longitude

  def get_daily_weather(self, latitude: str, longitude: str):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.api_key}&units={self.args.units}"
    weather_response = self._get(weather_url)
    
    return weather_response.json()

  def return_weather(self, weather_dict):
    temp = str(weather_dict['main']['temp'])
    temp_min = str(weather_dict['main']['temp_min'])
    temp_max = str(weather_dict['main']['temp_max'])
    wind_speed = str(weather_dict['wind']['speed'])
    weather_desc = str(weather_dict['weather'][0]['description'])
    return "Temp: " + temp + "\nTemp Min: " +  temp_min + "\nTemp Max: " + temp_max + "\nWind Speed: " + wind_speed + "\nWeather Description: " + weather_desc


if __name__ == "__main__":

  if not API_KEY:
    print("API key does not exist for open weather")
    sys.exit(1)

  parser = argparse.ArgumentParser(description= 'Generates current weather data')
  parser.add_argument('--zip', type=str, help="enter zipcode for weather data", required=True)
  parser.add_argument('--country', '-c', type=str, default='US', help="enter country abbreviation")
  parser.add_argument('--units', type=str, default='imperial', help="enter units")
  args = parser.parse_args()

  weather = Weather(args)
  latitude, longitude = weather._get_coord()
  weather_dict = weather.get_daily_weather(latitude, longitude)
  weather_results = weather.return_weather(weather_dict)
  
  print(weather_results)

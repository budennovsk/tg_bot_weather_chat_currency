# -*- coding: utf-8 -*-
from pprint import pprint

import requests
import json
from secret_key import API_KEY_YANDEX
from geopy import geocoders


class Weather:
    def __init__(self):
        self.condition = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                          'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                          'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                          'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                          'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                          'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                          'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                          }

    def geo_coordinats(self, city):
        if geocoders.Nominatim(user_agent="telebot"):
            geolocator = geocoders.Nominatim(user_agent="telebot")
            latitude = str(geolocator.geocode(city).latitude)
            longitude = str(geolocator.geocode(city).longitude)
            return latitude, longitude
        return f'Ошибка в запросе координат'

    def get_weather(self, city):
        lat, lon = self.geo_coordinats(city)

        URL = f'https://api.weather.yandex.ru/v2/forecast?'
        params = {
            'lat': lat,
            'lon': lon,
            'lang': 'ru_RU',
            'limit': '3'
        }
        headers = {
            'X-Yandex-API-Key': API_KEY_YANDEX
        }
        response = requests.get(URL, headers=headers, params=params)
        # pprint(response.json())
        if response.status_code == 200:
            response_data = {}
            data = response.json()
            response_data['def_pressure_mm'] = data.get('info').get('def_pressure_mm')
            response_data['temp_now'] = data.get('fact').get('temp')
            response_data['feels_like'] = data.get('fact').get('feels_like')
            response_data['geo_object'] = data.get('geo_object').get("locality").get("name")
            response_data['condition'] = self.condition[data.get('fact').get('condition')]
            response_data['forecasts'] = [i.get('parts').get('day').get('temp_avg') for i in data.get('forecasts')]

            return f'Город: {response_data["geo_object"]} \n' \
                   f'Температура воздуха сейчас: {response_data["temp_now"]}°С \n' \
                   f'Температура ощющается: {response_data["feels_like"]}°С \n' \
                   f'Температура Утро: {response_data["forecasts"][0]}°С, Полдень: {response_data["forecasts"][1]}°С, Вечер: {response_data["forecasts"][2]}°С \n'  \
                   f'Давление: {response_data["def_pressure_mm"]} мм/рт/ст \n' \
                   f'Осадки: {response_data["condition"]}'

            # with open('api.json', 'w') as file:
            #     json.dump(data, file, indent=4, ensure_ascii=False)
        return f'Ошибка в запросе API'


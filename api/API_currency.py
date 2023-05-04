# -*- coding: utf-8 -*-
from pprint import pprint

import requests

from secret_key import API_KEY_CURRENCY


class Currency:

    def get_currency(self,amount, from_cur, to_cur):
        URL = f'https://api.apilayer.com/exchangerates_data/convert?to={to_cur}&from={from_cur}&amount={amount}'

        headers = {'apikey': API_KEY_CURRENCY}

        response = requests.get(URL, headers=headers)
        data = response.json()

        if response.status_code == 200:
            date = data['date']
            rate = data['info']['rate']
            result = data['result']
            return f'Дата: {date}. \nПри переводе из {from_cur} в {to_cur} по курсу {rate} получится: {result} {to_cur}'
        else:
            return f'Не удалось получить курс. Ошибка: {data["error"]["message"]}'



# -*- coding: utf-8 -*-
from pprint import pprint

import requests
import io

from secret_key import API_KEY_PHOTO


class Photo:

    def get_photo(self):
        URL = 'https://api.api-ninjas.com/v1/randomimage?category=wildlife'
        headers = {'X-Api-Key': API_KEY_PHOTO,
                   'Accept': 'image/jpg'
                   }
        response = requests.get(URL, headers=headers)
        if response.status_code == 200:
            photo_file = io.BytesIO(response.content)
            return photo_file


        # file = io.open("whale.png", "wb", buffering=0)
        # file.write(response.content)

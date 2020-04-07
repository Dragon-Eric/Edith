#coding:utf-8

import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8') 

API = 'https://api.seniverse.com/v3/weather/now.json?'
KEY = 'SMLi1RmKQt1aUUKys'
LOCATION = 'xinyang'
LANGUAGE = 'zh-Hans'
UNIT = 'c'

def fetchWeather():
    result = requests.get(API, params={
        'key': KEY,
        'location': LOCATION,
        'language': LANGUAGE,
        'unit': UNIT
    }, timeout=1)
    return result.text

def getWeatherStr():
    result = fetchWeather()
    weather = json.loads(result)
    weather_str = weather['results'][0]['location']['name'] + '市当前天气为' + \
                  weather['results'][0]['now']['text'] + ',气温' + \
                  weather['results'][0]['now']['temperature'] + '度' 
    return weather_str


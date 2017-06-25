import requests

SITE_URL = 'http://taps-aff.co.uk'

def GetWeatherData(location):
    if not location:
        return None

    url = SITE_URL+'/?api&location=' + location
    weather_json = {}

    try:
        response = requests.get(url)
        weather_json = response.json()
    except requests.exceptions.ConnectionError:
        print ("Error retrieving data from " + url)

    return weather_json

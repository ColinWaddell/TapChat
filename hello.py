from flask import Flask, request, render_template
from helpers.weatherdata import GetWeatherData
import json
from datetime import date
import calendar

app = Flask(__name__)

# Load from template
def build_reponse(speech_text, card_title, card_content):
    with open('templates/default_response.json') as response_file:
        response = json.load(response_file)

    response["response"]["outputSpeech"]["text"] = speech_text
    response["response"]["card"]["title"] = card_title
    response["response"]["card"]["content"] = card_content

    return json.dumps(response)

def get_current_location(device_id, consent_tkn):
    URL = "https://api.eu.amazonalexa.com/v1/devices/%s/settings/address/countryAndPostalCode" % (device_id, )
    HEADER = {'Accept': 'application/json',
             'Authorization': 'Bearer {}'.format(consent_tkn)}

    r = requests.get(URL, headers=HEADER)
    if r.status_code == 200:
        data = r.json()
        try:
            return data["city"]
        except KeyError:
            return

def subtract_days(frm, to):
    day_num = {  "Monday": 0, "Tuesday": 1, "Wednesday": 2,
               "Thursday": 3,  "Friday": 4,  "Saturday": 5,
                 "Sunday": 6}
    gap = day_num[to] - day_num[frm]

    if (gap < 1):
        gap += 7

    return gap

def process_request(request_data):
    response_error = build_reponse("Sorry, I made an arse of the request",
                           "TapsAff?",
                           "Error getting weather")
    # Decode the request
    try:
        request = json.loads(request_data)
    except json.JSONDecodeError:
        return response_error

    # Try and grab location
    try:
        location = request["request"]["intent"]["slots"]["Location"]["value"]
    except KeyError:
        try:
            device_id = request["context"]["System"]["device"]["deviceId"]
            consent_tkn = request["context"]["System"]["user"]["permissions"]["consentToken"]
            location = get_current_location(device_id, consent_tkn)
        except KeyError:
            # Can't find location
            return response_error

    try:
        weather = GetWeatherData(location)
        try:
            # Try and grab the day
            day = request["request"]["intent"]["slots"]["Day"]["value"]
            # How far into the forecast array do
            # I need to go?
            today = calendar.day_name[date.today().weekday()]
            forecast_n = subtract_days(today, day)
            taps_status = weather["forecast"][forecast_n]["taps"]
            return build_reponse("It is currently taps %s in %s on %s" % (taps_status, location, day),
                                   "TapsAff?",
                                   "Card stuff")
        except KeyError:
            # No day specified
            taps_status = weather["taps"]
            return build_reponse("It is currently taps %s in %s" % (taps_status, location),
                                   "TapsAff?",
                                   "Card stuff")

    except (KeyError, IndexError):
        return response_error

# Default request handler
@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return process_request(request.data)
    else:
        return render_template('hello.html')

# In order to simplify debugging you can
# just visit /test to get an interface
# to submit sample json, just like in
# the alexa developers test panel
@app.route('/test')
def test_page():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)

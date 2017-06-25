from flask import Flask, request, render_template
from helpers.weatherdata import GetWeatherData
import json

app = Flask(__name__)

# Load from template
def build_reposonse(speech_text, card_title, card_content):
    with open('templates/default_response.json') as response_file:
        response = json.load(response_file)

    response["response"]["outputSpeech"]["text"] = speech_text
    response["response"]["card"]["title"] = card_title
    response["response"]["card"]["content"] = card_content

    return json.dumps(response)

def get_current_location(device_id):
    url = "https://api.eu.amazonalexa.com/v1/devices/%s/settings/address/countryAndPostalCode" % (device_id, )

def process_request(request_data):
    response_error = build_reposonse("Sorry, I made an arse of the request",
                           "TapsAff?",
                           "Error getting weather")
    # Decode the request
    try:
        request = json.loads(request_data)
    except JSONDecodeError:
        return response_error

    # Try and grab location
    try:
        location = request["request"]["intent"]["slots"]["Location"]["value"]
    except KeyError:
        location = ""

    # Try and grab day
    try:
        day = request["request"]["intent"]["slots"]["Day"]["value"]
    except KeyError:
        day = ""

    try:
        weather = GetWeatherData(location)
        if(day):
            # How far into the forecast array do
            # I need to go?
        else:
            taps_status = weather["taps"]
            return build_reposonse("It is currently taps %s in %s" % (taps_status, location),
                                   "TapsAff?",
                                   "Card stuff")

    except KeyError:
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

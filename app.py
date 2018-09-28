#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from textblob import TextBlob
from bs4 import BeautifulSoup
import requests

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    result = req.get("result")
    parameters = result.get("parameters")
    term = parameters.get("geo-city")

    sentiment = 0
    subjectivity = 0
    url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format(term)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headline_results = soup.find_all('div', class_='st')
    for text in headline_results:
        blob = TextBlob(text.get_text())    
        sentiment += blob.sentiment.polarity / len(headline_results)
        subjectivity += blob.sentiment.subjectivity / len(headline_results)
    res = makeWebhookResult(data)
    return res


def makeWebhookResult(data):

    speech = "Today is good"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

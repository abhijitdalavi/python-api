#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import requests

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # print("Request:")
    # print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    meta = req.get("queryResult")
    term = meta.get("queryText")

    sentiment = 0
    subjectivity = 0.
    url = 'http://program-o.com/v3/chat.php?say={0}'.format(term)
    response = requests.get(url)
    data_dict = json.loads(response.text)
    res_text = data_dict["conversation"]["say"]["bot"]
    res = makeWebhookResult(res_text)
    return res


def makeWebhookResult(data):

    speech = data

    print("Response:")
    print(speech)

    return {
        "fulfillmentText": speech,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

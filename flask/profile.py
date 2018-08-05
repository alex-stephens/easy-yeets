# -*- coding: UTF-8 -*-

import requests
import json
uri = 'https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAATAzyZCOs18BALOYCxbRFNTZA2A0bmROsrBx2oWpIbXjRuyBPHo0B4B25YonmGOgCOa7jD7fDmVhVjuZB9Py4BdogYadrk8LEgZCFRHb5xHKDSL3cywsZAGJiNIH4ITbo4Nr8PxKZAzonUNemMcLINBK8GtaoRpj7dKCjqB3eFgZDZD'


def delete_field():
    pass

def send_data(data) :
    r = requests.post(uri, headers = {"Content-Type": "application/json"}, data = data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

send_data(json.dumps({
  "persistent_menu":[
    {
      "locale":"default",
      "composer_input_disabled": False,
      "call_to_actions":[
        {
          'title': 'Food near me 🍔',
          "type":"postback",
          'payload': 'hungryButton',
        },
        {
        'type': 'postback',
        'title': 'What\'s hot? 🔥',
        'payload': 'browseButton',
        },
        {
        'type': 'postback',
        'title': 'My Places ❤️',
        'payload': 'placesButton'
        }


          ]
        }
      ]
    }))

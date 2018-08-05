# -*- coding: UTF-8 -*-
from __future__ import print_function

import os
import sys
import json
import restData
from datetime import datetime

#import gmapsQuery as gq

import requests
from flask import Flask, request

import pickle

rid = 0
app = Flask(__name__)

users = {}
userLookup = {}
restDict = {}

restLookup = {}


class Rest:

    def __init__(self, name, foodURLs, coords):
        global rid
        self.name = name
        self.foodURLs = foodURLs
        self.id = rid
        self.coords = coords
        rid += 1

class User:

    def __init__(self, id) :
        self.id = id
        self.state = 'start'
        self.restRank = 0

    def at_start(self) :

        gen_send_message(self.id, {
            'text': 'Hey here!\nWhat are you looking for?',
            'quick_replies': [
                {
                'content_type': 'text',
                'title': 'I\'m hungry 🍔',
                'payload': 'hungryButton',
                },
                {
                'content_type': 'text',
                'title': 'What\'s hot? 🔥',
                'payload': 'browseButton',
                },
                {
                'content_type': 'text',
                'title': 'My Places ❤️',
                'payload': 'placesButton'
                }
            ]
        })
    def at_askLoc(self) :
        gen_send_message(self.id, {
            'text': 'Awesome - Collecting some cool places now 😎'
        })
        gen_send_message(self.id, {
            'text': 'Please share your location',
            'quick_replies': [
                {
                    'content_type': 'location'
                }
            ]
        })

    def do_directions(self, restId) :
        global restDict
        print(restDict)
        rest = restDict[int(restId)]
        mapUrl = gen_map_url(*rest.coords)
        #print(rest.coords, mapUrl)
        gen_send_message(self.id, {
            "attachment":{
                "type":"template",
                "payload": {
                    "template_type":"generic",
                    "image_aspect_ratio": "square",
                    'elements': [{
                    'title':rest.name,
                    'image_url':mapUrl,
                    'default_action':{
                        'type':'web_url',
                        'url': 'www.google.com'
                        }
                    }
                    ]
                }
            }
        })

    def ask_food_type(self) :
        gen_send_message(self.id, {
            'text': 'What are you looking for?',
            'quick_replies':[
            gen_text_quick_reply('Coffee', 'coffeeButton'),
            gen_text_quick_reply('Breakfast', 'breakfastButton'),
            gen_text_quick_reply('Lunch', 'lunchButton'),
            gen_text_quick_reply('Dinner', 'dinnerButton'),
            ]
        })
    def at_sendRest(self) :

        gen_send_message(self.id, {
            'text': 'Here are some places near you' if self.restRank else 'How about these places?'
        })
        restList = []
        global restLookup
        i = 0
        for key in restLookup:
            restList.append(restLookup[key]['place_id'])
            i += 1
            if i >= 3:
                break

        print('Rest list:' + str(restList))

#        rests = [
#            Rest('Alice\'s Thai', [
#                'https://images.pexels.com/photos/1234535/pexels-photo-1234535.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
#                'https://images.pexels.com/photos/46247/thai-food-noodle-fried-noodles-meal-46247.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
#                'https://images.pexels.com/photos/262897/pexels-photo-262897.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260'
#            ],(-33.892871,151.1846416)),
#            Rest('Guzman y Gomez', [
#            'https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
#            'https://images.pexels.com/photos/5944/food-lunch-mexican-nachos.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
#            'https://images.pexels.com/photos/58722/pexels-photo-58722.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260'
#            ], (-33.883448,151.1938926))
#        ]
#
#        global restDict
#
#        restDict = {r.id : r for r in rests}
#
#        try :
#            restList = restData.restFromLatLon((self.lat, self.long))
#        except Exception as e:
#            print(e)
#            self.at_askLoc()
#            return

#        global restLookup
#        print(restLookup)
        restDatas = []
        for r in restList:
            try:
                restDatas.append(restLookup[r])
            except Exception as e:
                print('Error on:'
                , e, r)
        print(restList)


#        for r in rests:
        for r in restDatas:
            gen_send_message(self.id, {
            'text': r['name']
            })
            gen_send_message(self.id, {
                "attachment":{
                    "type":"template",
                    "payload": {
                        "template_type":"generic",
                        "image_aspect_ratio": "square",
                        'elements': [

                        generate_element(r['name'],r['image_url'][0], 'Rating', r['rating'])] +
                        [
                        {
                        "title": r['name'],
                        "image_url": url,
                        } for url in r['image_url'][1:]

                        ]
                    }
                },
                'quick_replies': [
                    {
                    'content_type': 'text',
                    'title': "I don't like these...",
                    'payload': 'moreButton',
                    }
                ]
            })
        self.restRank += 3
        # gen_send_message(self.id, {
        #     'quick_replies': [
        #         {
        #         'content_type': 'text',
        #         'title': "I don't like these...",
        #         'payload': 'moreButton',
        #         }
        #     ]
        # })
        # #send_cards(self.id, None)

def gen_text_quick_reply(text, payload) :
    return {
    'content_type': 'text',
    'title': text,
    'payload': payload,
    }

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/.well-known/acme-challenge/4lXc_9u7zKQhsMRegC8LVILkkx2ILck9VuxKsVJzGwY', methods=['GET'])
def secure():
    return '4lXc_9u7zKQhsMRegC8LVILkkx2ILck9VuxKsVJzGwY.5jd19jyXESABNabDBciM0z8c2Nn0tz4bUXIVmP_bGe8'

@app.route('/', methods=['GET'])
def main():
    return 'hello world'


def send_names(sender_id, lat, long) :
#    rests = gq.get_near(lat, long)
    names = [r['name'] for r in rests]
    send_message(sender_id, '\n'.join(str(n) for n in names))

def on_message_event(curUser, event) :

    messaging_event = event
    sender_psid = messaging_event['sender']['id']

    # Save our data to a textfile
    save_db()

    if 'message' in event:
        message = event['message']
    else:
        print('Error no message')
        return

    if 'quick_reply' in message:

        payload = message['quick_reply']['payload']
        if payload == 'hungryButton' or payload == 'browseButton':
            curUser.state = 'askType'
            curUser.ask_food_type()
            return
        types = ['coffeeButton', 'breakfastButton', 'lunchButton', 'dinnerButton']
        if payload in types:
            curUser.foodType = payload
            curUser.state = 'askLoc'
            curUser.at_askLoc()
            return
        if 'directionButton' in payload:
            curUser.give_directions()
        if 'moreButton' == payload:
            curUser.at_sendRest()
    elif 'attachments' in event['message']:
        attachments = event['message']['attachments']
        if 'payload' in attachments[0] and 'coordinates' in attachments[0]['payload']:
            coordinates = attachments[0]['payload']['coordinates']
            lat = coordinates['lat']
            long = coordinates['long']
            curUser.lat = lat
            curUser.long = long
            curUser.state = 'sendRest'
            curUser.at_sendRest()
            return


    if curUser.state == 'start':
        curUser.at_start()
        return

    return


def handle_postback(curUser, postback) :
    print('Postback for: ', curUser.id)
    if postback.get('payload') :
        payload = postback['payload']
        if 'directionButton' in payload:
            resId = payload[len('directionButton'):]
            curUser.do_directions(resId)
        if payload in ['hungryButton', 'browseButton']:
            curUser.at_askLoc()

@app.route('/webhook', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    #print(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                sender_psid = messaging_event['sender']['id']

                if sender_psid not in users:
                    users[sender_psid] = User(sender_psid)

                # store some data for the user
                if sender_psid not in userLookup:
                    userLookup[sender_psid] = {}

                curUser = users[sender_psid]

                print('Cur user: ' + curUser.id)

                print('EVENT:', json.dumps(messaging_event, indent = 2))

                if messaging_event.get('message'):
                    on_message_event(curUser, messaging_event)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    handle_postback(curUser, messaging_event.get('postback'))

    return "ok", 200


def send_quick_reply(recipient_id, replies) :
    gen_send_message(recipient_id, {
        "text": "here is a quick reply",
        "quick_replies": replies
    })

def send_cards(id, payload) :
    payload = {
            "template_type":"generic",
            "image_aspect_ratio": "square",
            "elements": [
                generate_element('Meme', 'https://slack-redir.net/link?url=https%3A%2F%2Finstagram.fsyd2-1.fna.fbcdn.net%2Fvp%2F3f173cc1a8e75678e01633e9a119b518%2F5C09AE06%2Ft51.2885-15%2Fe35%2F37718109_661277254238317_4937345028814012416_n.jpg%3Fse%3D7%26ig_cache_key%3DMTgzNzY3NDE3NzgyNDI0ODMwMw%253D%253D.2','subtitle')
                ,
                generate_element('Meme2', 'https://slack-redir.net/link?url=https%3A%2F%2Finstagram.fsyd2-1.fna.fbcdn.net%2Fvp%2F3f173cc1a8e75678e01633e9a119b518%2F5C09AE06%2Ft51.2885-15%2Fe35%2F37718109_661277254238317_4937345028814012416_n.jpg%3Fse%3D7%26ig_cache_key%3DMTgzNzY3NDE3NzgyNDI0ODMwMw%253D%253D.2','subtitle')
            ]
    }
    gen_send_message(id, {
        "attachment":{
            "type":"template",
            "payload": payload
        }
    })
def get_tags():
    #POST https://vision.googleapis.com/v1/images:annotate?key=YOUR_API_KEY
    pass
def gen_map_url(lat, long):
    format = "terrain" # terrain, roadmap, satellite, hybrid
    size = 600
    size_str = str(size) + "x" + str(size)

    url = "https://maps.googleapis.com/maps/api/staticmap?center=" + str(lat) + \
    "," + str(long) + "&zoom=16&scale=false&size=" + size_str + "&maptype=" + format + \
    "&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:%7C{},{}".format(lat, long)
    return url
def generate_element(title, image_url, subtitle, id):
    element = {
        "title":title,
        "image_url":image_url,
        "subtitle":"⭐⭐⭐⭐",
        # "default_action": {
        #     "type": "web_url",
        #     "url": "https://www.google.com",
        #     "webview_height_ratio": "full",
        #     },
        "buttons":[
            {
                "type":"web_url",
                "url":"https://www.google.com",
                "title":"Show More Photos"
            },{
                    "type":"postback",
                    "title":"Directions",
                    "payload":"directionButton"+str(id)
            },{
                "type": "element_share",
                "share_contents": {
                  "attachment": {
                    "type": "template",
                    "payload": {
                      "template_type": "generic",
                      "elements": [
                        {
                          "title": title,
                          "subtitle": "⭐⭐⭐⭐",
                          "image_url": image_url,
                          "default_action": {
                            "type": "web_url",
                            "url": "http://m.me/petershats?ref=invited_by_24601"
                          },
                          "buttons": [
                            {
                              "type": "web_url",
                              "url": "http://m.me/petershats?ref=invited_by_24601",
                              "title": "Take Quiz"
                            }
                          ]
                        }
                      ]
                    }
                  }
                 }
                }
        ]

    }

    return element

def gen_send_message(id, message) :
    print("sending message to", id)

    params = {
        "access_token": "EAATAzyZCOs18BALOYCxbRFNTZA2A0bmROsrBx2oWpIbXjRuyBPHo0B4B25YonmGOgCOa7jD7fDmVhVjuZB9Py4BdogYadrk8LEgZCFRHb5xHKDSL3cywsZAGJiNIH4ITbo4Nr8PxKZAzonUNemMcLINBK8GtaoRpj7dKCjqB3eFgZDZD"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": id
        },
        "message": message
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

def get_params() :
    return {
        "access_token": "EAATAzyZCOs18BALOYCxbRFNTZA2A0bmROsrBx2oWpIbXjRuyBPHo0B4B25YonmGOgCOa7jD7fDmVhVjuZB9Py4BdogYadrk8LEgZCFRHb5xHKDSL3cywsZAGJiNIH4ITbo4Nr8PxKZAzonUNemMcLINBK8GtaoRpj7dKCjqB3eFgZDZD"
    }
def get_headers():
    return {
        "Content-Type": "application/json"
    }


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": "EAATAzyZCOs18BALOYCxbRFNTZA2A0bmROsrBx2oWpIbXjRuyBPHo0B4B25YonmGOgCOa7jD7fDmVhVjuZB9Py4BdogYadrk8LEgZCFRHb5xHKDSL3cywsZAGJiNIH4ITbo4Nr8PxKZAzonUNemMcLINBK8GtaoRpj7dKCjqB3eFgZDZD"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text": message_text,
                    "buttons":[
                        {
                            "type":"web_url",
                            "url":"https://www.messenger.com",
                            "title":"Visit Messenger"
                        }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

def add_to_favourites(user_id, place_id):

    if 'favourites' not in userLookup[user_id]:
        userLookup[user_id]['favourites'] = [];

    userLookup[user_id]['favourites'] += place_id;

def rate_place(user_id, place_id, rating):
    userLookup[user_id][place_id]['rating'] = rating

    if 'visited' not in userLookup[user_id]:
        userLookedup[user_id][place_id]['visited'] = 0

    userLookup[user_id][place_id]['visited'] += 1;
   
    if 'user_rating' not in restLookup[place_id]:
        restLookup[place_id]['user_rating'] = 0
    if 'visited' not in restLookup[place_id]:
        restLookup[place_id]['visited'] = 0

    restLookup[place_id]['user_rating'] += rating
    restLookup[place_id]['visited'] += 1

def save_db():
    with open("rest_updated.txt", "wb") as file: 
        pickle.dump(restLookup, file)

    with open("user_db_updated.txt", "wb") as file: 
        pickle.dump(userLookup, file)

def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print(u"{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    restLookup = restData.get_rest_dict()
    userLookup = restData.get_user_dict()

    app.run(host='0.0.0.0', port=80, debug=True)

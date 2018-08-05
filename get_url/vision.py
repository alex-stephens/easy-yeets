import io
import pickle
import os
import base64
import requests
import urllib

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

restUrlDict = pickle.load(open("rest_url.txt","rb"))

import pdb
pdb.set_trace()

for k in reversed(range(len(restUrlDict))):
    print k
    d = restUrlDict[k]
    for i in reversed(range(len(d['image_url']))):
        print i
        url = d['image_url'][i]
        opener = urllib.urlopen(url)
        content = opener.read()
        image = vision.types.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        found = False
        for j in range(min(5, len(labels))):
            if labels[j].description.find("food") != -1:
                found = True
                break
        if not found:
            print "POP {}".format(i)
            d['image_url'].pop(i)
        else:
            print "Good"
    if len(d['image_url']) < 3:
        print "POP WHOLE LIST {}".format(k)
        restUrlDict.pop(k)
    print "k with len {}".format(len(restUrlDict))

with open("rest_google_vision.txt", "wb") as myfile:
    pickle.dump(restUrlDict, myfile, protocol=2)


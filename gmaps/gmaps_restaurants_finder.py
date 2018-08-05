import googlemaps
import time
import pickle
from datetime import datetime
import json


gmaps = googlemaps.Client(key='AIzaSyDAOpH3KzlnMy45taoxIKMvDj23q4uneTI')
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
geocode_result[0]['geometry']['location']
# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
page_token = None;
with open("restaurants.txt", "w") as myfile:
    place_data = []
    for i in range(0, 50):
        print i
        print page_token
        places_result = gmaps.places_nearby(location=(-33.865586,151.205439),
                rank_by="distance",
                type="restaurant",
                open_now=False,
                page_token=page_token
                )
        time.sleep(2)
        results = places_result['results']

        import pdb
        pdb.set_trace()
        place_data = place_data + [{
            'name': p['name'],
            'place_id':p['place_id'],
            'types': p['types']
        } for p in results]
        try:
            page_token = places_result['next_page_token']
        except:
            break;

    pickle.dump(place_data, myfile, protocol=2)

def restFromLatLon(location):


    places_result = gmaps.places('food near me',
            location=location,
            open_now=True,
            )
    results = places_result['results']

    place_data = [ p['name'] for p in results]

    return place_data





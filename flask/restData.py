from __future__ import print_function
import pickle
import googlemaps
#
# def get_rest_dict():
#     restData = pickle.load(open('restaurants_zomato.txt'))
#     # print(len(restData))
#     # print([r['name'] for r in restData], sep = '\n')
#     return {r['name'] : r for r in restData}
#
#
# def restFromLatLon(location):
#
#     gmaps = googlemaps.Client(key='AIzaSyDAOpH3KzlnMy45taoxIKMvDj23q4uneTI')
#
#     places_result = gmaps.places('food near me',
#             location=location,
#             open_now=True,
#             )
#     results = places_result['results']
#
#     place_data = [ p['name'] for p in results]
#
#     return place_data
def get_rest_dict():
    return pickle.load(open('rest_google_vision_dict.txt', 'rb'))
    # print(len(restData))
    # print([r['name'] for r in restData], sep = '\n')
    #return {r['name'] : r for r in restData}


def restFromLatLon(location):

    gmaps = googlemaps.Client(key='AIzaSyDAOpH3KzlnMy45taoxIKMvDj23q4uneTI')

    places_result = gmaps.places('food near me',
            location=location,
            open_now=True,
            )
    results = places_result['results']

    place_data = [ p['name'] for p in results]

    return place_data

def get_user_dict():
    return pickle.load(open('user_db.txt', 'rb'))

    #return {r['name'] : r for r in userData}

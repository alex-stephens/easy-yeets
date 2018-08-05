import requests
import pickle
import json


def getZomatoData(searchStr):
    payload = {
        'q': searchStr
    }
    headers = {'user-key': 'fe6428083779eb2109cd0ff75bba7b9d'}
    result = requests.get('https://developers.zomato.com/api/v2.1/search', params=payload, headers=headers).json()['restaurants'][0]['restaurant']
    rating = '3'
    average_cost_for_two = 40
    price_range = 2
    try:
        rating = result['user_rating']['aggregate_rating']
    except:
        rating = '3.0'

    try:
        average_cost_for_two = result['average_cost_for_two']
    except:
        average_cost_for_two = 40

    try:
        price_range = result['price_range']
    except:
        price_range = 2

    try:
        cuisine = result['cuisine']
    except:
        cuisine = 'Food'

    return {
        'rating':rating,
        'average_cost_for_two':average_cost_for_two,
        'price_range': price_range,
        }

def main():
    list_dict = pickle.load(open("restaurants.txt", "rb"))

    print len(list_dict)
    for i in reversed(range(0,len(list_dict))):
        print i
        try:
            d = list_dict[i]
            name = d['name']
            result = getZomatoData(name)
            d['rating'] = result['rating']
            d['average_cost_for_two'] = result['average_cost_for_two']
            d['price_range'] = result['price_range']
        except:
            list_dict.pop(i)

    print len(list_dict)
    with open("rest_.txt", "w") as myfile:
        pickle.dump(list_dict, myfile, protocol=2)

main()

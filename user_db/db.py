# Users session
# users['fb_id'] = {
#       restaurants:  {
#           place_id: {
#               rating: x
#               visited: x
#
#                }
#           favourites: [ <place_id's> ] # or possibly just return by highest rated (look @ uber eats)l
#    }
# }

def addToFavourites(user_id, place_id):
    users[user_id]['favourites'] += place_id;

def ratePlace(user_id, place_id, rating):
    users[user_id][place_id]['rating'] = rating
    users[user_id][place_id]['visited'] += 1
    rest[place_id]['user_rating'] = rating;
    rest[place_id]['visit_rate'] += 1;

# Keep track of how many time a restaurant is visited ('popular this week' near you (look at uber eats))

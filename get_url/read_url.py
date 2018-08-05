import pickle

dict = pickle.load(open("rest_google_vision.txt","rb"))

rest = {r['place_id'] : r for r in dict}

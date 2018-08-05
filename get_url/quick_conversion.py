import pickle

dic = pickle.load(open("rest_google_vision.txt", "rb"))

new_dic = {r['place_id'] : r for r in dic}


with open("rest_google_vision_dict.txt", "wb") as file:
    pickle.dump(new_dic, file, protocol=2)

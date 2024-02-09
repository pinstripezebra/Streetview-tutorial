import requests
import googlemaps
import os
import pandas as pd
import random


def pull_image(gmaps,  address,parent_folder,city_count, name = ""):

    """Takes an addres string as an input and returns an image from google maps streetview api"""
    pic_base = 'https://maps.googleapis.com/maps/api/streetview?'

    # define the params for the picture request
    pic_params = {'key': google_api_key,
              'location': address,
              'size': "500x500"}
    
    #Requesting data
    pic_response = requests.get(pic_base, params=pic_params)
    image_name = name + "_ " + str(city_count) + ".jpg"
    with open(parent_folder +"Data\\Images\\"+ image_name, "wb") as file:
        file.write(pic_response.content)
    
    # Closing connection to API
    pic_response.close()

if __name__ == "__main__":

    #Storing latitude/longitude of pictures so we dont pull the same one twice
    lat_long = []
    random.seed(4)
    parent_folder = os.path.dirname(os.path.dirname(__name__))
    google_api_key = open(parent_folder + "api_key.txt", "r").read()
    cities = pd.read_csv(parent_folder + "Data//CityList.csv")
    gmaps = googlemaps.Client(key=google_api_key)

    # Pulling 1 image
    
    pull_image(gmaps,  "400 Broad St, Seattle, WA 98109",
               parent_folder,1, name = "")
    
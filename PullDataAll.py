import requests
import googlemaps
import os
import pandas as pd
import random

#from random import seed

def convert_long_lat_to_address(gmaps,location):

    """Converts a latitude/longitude tuple into an address string, returns string"""

    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode(location)
    geocode_components = reverse_geocode_result[0]
    coms = geocode_components['address_components']

    #Breaking down geocode results
    street_number = coms[0]['long_name']
    street_name = coms[1]['long_name']
    city = coms[3]['long_name']
    state = coms[5]['long_name']
    country = coms[6]['long_name']
    postal_code = coms[7]['long_name']

    #Assembling into address
    address = street_number +" "+ street_name +" "+ city +" "+ state +" "+ country +" "+ postal_code

    return city,address

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

def query_random_location(gmaps, location, parent_folder, lat_long,name = "", min_distance = 0.005):

    """
    Takes input city coordinates, adds a random element, and pulls an image from this location
    ------------------
    INPUT:
        gmaps: Google maps object
        location: tuple containing latitude and longitude
        parent_folder: str containing reference to parent folder
        lat_long: list containing all previously called coordinates
        min_distance: float containing minimum distance allowable between new old/new coordiantes
    ------------------
    OUTPUT:
        None
    """

    #One degree Latitude = 64 miles, taking 1/100 of that
    random_multiplier = 0.05

    #Generates random value in range [-0.005, 0.005]
    random_lat = (random.random()-0.5) * random_multiplier
    random_long = (random.random()-0.5) * random_multiplier

    original_lat, original_long = list(location)[0], list(location)[1]
    #Calculating new latitude and longitude values
    new_lat, new_long = round(original_lat + random_lat,6), round(original_long + random_long,6)

    #Ensuring new coordinates sufficiently far from old oness
    while (round(new_lat,3), round(new_long,3)) in guessed_coordinates:
        print('redo', [new_lat, new_long])
        random_lat = (random.random()-0.5) * random_multiplier
        random_long = (random.random()-0.5) * random_multiplier
        new_lat, new_long = round(original_lat + random_lat,6), round(original_long + random_long,6)

    guessed_coordinates.append((round(new_lat,3), round(new_long,3)))

    #Adding coordinate set to previously called list
    lat_long.append((round(new_lat, 4), round(new_long, 4)))
    new_location = (new_lat, new_long)

    #Calling functions
    try:
        city, address = convert_long_lat_to_address(gmaps,new_location)
        pull_image(gmaps, address,parent_folder,str(new_location), name)
    except:
        print("No Image for Location")

def query_multiple_locations(cities, return_count, parent_folder, lat_long):

    """Takes list of cities and returns return_count of images from each"""
    for index, row in cities.iterrows():
        location = (row['Latitude'], -row['Longitude'])
        for count in range(return_count):
            query_random_location(gmaps, location, parent_folder, lat_long, row['City'])




if __name__ == "__main__":

    #Storing latitude/longitude of pictures so we dont pull the same one twice
    lat_long = []
    random.seed(4)
    parent_folder = os.path.dirname(os.path.dirname(__name__))
    google_api_key = open(parent_folder + "api_key.txt", "r").read()
    cities = pd.read_csv(parent_folder + "Data//CityList.csv")
    gmaps = googlemaps.Client(key=google_api_key)
    return_count = 200

    guessed_coordinates = []
    #Iterating through cities
    query_multiple_locations(cities, return_count, parent_folder, lat_long)
    print("Done")

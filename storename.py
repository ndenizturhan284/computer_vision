#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 16:03:02 2020

@author: ndenizturhan
"""

import json
import urllib
import geopy.distance
import csv

def callAPI(latlonArray):
    latlon = str(latlonArray[0]) + "," + str(latlonArray[1])
    #radius in meters
    radius = "10"
    key="AIzaSyCuu8pFPZLLg4ZNlweRUkG38tQvMNgQ8is"
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + latlon + "&radius=" + radius + "&key=" + key
    r = urllib.request.urlopen(url)
    data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    
    output_file = "/home/ndenizturhan/Downloads/test.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    minDist = 99999999999
    ll = []
    for ar in data["results"]:
        name = ar["name"]
        lat = ar["geometry"]["location"]["lat"]
        lon = ar["geometry"]["location"]["lng"]
        dist = geopy.distance.distance([lat, lon], [float(latlon.split(",")[0]), float(latlon.split(",")[1])]).km*1000
        if dist < minDist:
            minDist = dist
            #ll = [lat, lon]
            ll=name
    return ll

doorLL = []
count = 0 #used to limit how many doors i get from csv
with open("/home/ndenizturhan/Downloads/latlon.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 
    for row in csvreader:
        if(row[1] == "1" and row[3] != "0" and row[4] != "0"):
            doorLL.append((float(row[3]), float(row[4])))
            count+=1
            #if count == 100:
              # break

storeLL = []
for ll in doorLL:
    storeLL.append(callAPI(ll))

print(doorLL)
print(storeLL)

import pandas as pd
doordt=pd.DataFrame(doorLL, columns=["lat", "lon"])
doordt["name"]=storeLL
print(doordt)

doordt.to_csv('store_names_full.csv', index=False,header=["lat", "lon"])
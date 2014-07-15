import json
import ast
import sqlite3
from sqlite3 import *

from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
import numpy as np
from pandas import DataFrame
import pandas
from sklearn import linear_model
from sklearn.externals import joblib
from pygeocoder import Geocoder
from Rest_Farmington.models import Rest_Farmington_Hills


import compare_restaurants as cp
import getDistance

def hello(request):
	return render_to_response('index.html')

def maps(request):
	lat1=[]
	lon1=[]
	if 'restaurant' in request.GET and 'zipcode' in request.GET and 'miles' in request.GET:
		restaurant=request.GET['restaurant']
		zipcode=request.GET['zipcode']
		miles=request.GET['miles']
		lattitude,longitude=getDistance.findLocation(zipcode)
		lat1=lattitude
		lon1=longitude
		cp.compare_restaurants(restaurant, lattitude,longitude,miles)
	con=connect("restinfo.db")
	c = con.cursor()
	x1=c.execute("SELECT * FROM RESTAURANTS_MATCH " )
	x=c.fetchall()
	restaurant=[]
	longitude=[]
	lattitude=[]
	address=[]
	distance=[]
	for y in x:
		i=1
		restaurants=y[0]
		longitudes=y[2]
		lattitudes=y[1]
		addresses=y[3]
		distances=getDistance.findDistance(lat1,lon1,lattitudes,longitudes)
		restaurant.append(restaurants)
		address.append(addresses)
		distance.append(distances)
		i+=1
	s= sorted(range(len(distance)), key=lambda k: distance[k])
	print s
	print restaurant
	result={'restaurant_1':restaurant[s[0]],'restaurant_2':restaurant[s[1]],'restaurant_3':restaurant[s[2]],'restaurant_4':restaurant[s[3]],\
		'restaurant_5':restaurant[s[4]],'address_1':address[s[0]],'address_2':address[s[1]],'address_3':address[s[2]],\
		'address_4':address[s[3]],'address_5':address[s[4]]}
	print result
	return render(request,'maps.html',result)

def restaurant(request):
	restaurant = request.GET.get("restaurant")
	miles = request.GET.get("miles")
	zipcode = request.GET.get("zipcode")
	return result

def list_restaurants(restaurant,zipcode,miles):
	if 'restaurant' in request.GET and 'zipcode' in request.GET and 'miles' in request.GET:
		restaurant=request.GET['restaurant']
		zipcode=request.GET['zipcode']
		miles=request.GET['miles']
	else:
		return HttpResponse('You submitted an empty form.')

funcs = {
        "restaurants": list_restaurants
}

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3306)   

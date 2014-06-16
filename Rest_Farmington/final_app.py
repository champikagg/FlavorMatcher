import json
import ast
import MySQLdb

#Third party modules
from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
import numpy as np
from pandas import DataFrame
import pandas
from sklearn import linear_model
from sklearn.externals import joblib
from pygeocoder import Geocoder
from Rest_Farmington.models import Rest_Farmington_Hills


#import get_restaurants
#import logistic_regression
import compare_restaurants as cp
import getDistance
#import restaurants_match


def hello(request):
	return render_to_response('Rest_Farmington/index.html')

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
	con = MySQLdb.Connect(user='champika',host='localhost',passwd='mynewproject',db='restinfo')
	c = con.cursor()
	#c.execute("SET global wait_timeout=30000000;")
	#c.execute("SET session wait_timeout=30000000;")
	x1=c.execute("SELECT * FROM RESTAURANTS_MATCH " )
	x=c.fetchall()
	restaurant=[]
	longitude=[]
	lattitude=[]
	distance=[]
	for y in x:
		i=1
		restaurants=y[0]
		longitudes=y[1]
		lattitudes=y[2]
		distances=getDistance.findDistance(lat1,lon1,lattitudes,longitudes)
		restaurant.append(restaurants)
		longitude.append(longitudes)
		lattitude.append(lattitudes)
		distance.append(distances)
		i+=1
	s= sorted(range(len(distance)), key=lambda k: distance[k])
	#print s[0]
	result={'restaurant_1':restaurant[s[0]],'restaurant_2':restaurant[s[1]],'restaurant_3':restaurant[s[2]],'restaurant_4':restaurant[s[3]],\
	'longitude_1':longitude[s[0]],'longitude_2':longitude[s[1]],'longitude_3':longitude[s[2]],'longitude_4':longitude[s[3]],\
	'lattitude_1':lattitude[s[0]],'lattitude_2':lattitude[s[1]],'lattitude_3':lattitude[s[2]],'lattitude_4':lattitude[s[3]]}
	print result
	return render(request,'Rest_Farmington/maps.html',result)
	#if 'restaurant' in request.GET and 'zipcode' in request.GET and 'miles' in request.GET:
	#	restaurant=request.GET['restaurant']
	#	zipcode=request.GET['zipcode']
	#	miles=request.GET['miles']
	#	message = 'You entered restaurant: %r and city : %r ' % (restaurant, zipcode)
	#	cp.compare_restaurants(restaurant)
	#	#return render(request,'Rest_Farmington/maps.html',{'restaurant':restaurant,'zipcode':zipcode,'miles':miles})
	#	return render(request,'Rest_Farmington/maps.html',{'restaurant':restaurants_match.objects.all()})

def restaurant(request):
    #Get input arguments
	restaurant = request.GET.get("restaurant")
	miles = request.GET.get("miles")
	zipcode = request.GET.get("zipcode")
	#result=cp.compare_restaurants(restaurant)
	return result

#Get list of restaurants for typeahead
def list_restaurants(restaurant,zipcode,miles):
	if 'restaurant' in request.GET and 'zipcode' in request.GET and 'miles' in request.GET:
		restaurant=request.GET['restaurant']
		zipcode=request.GET['zipcode']
		miles=request.GET['miles']
		#cp.compare_restaurants(restaurant)
	else:
		return HttpResponse('You submitted an empty form.')

funcs = {
        "restaurants": list_restaurants
}

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3306)   

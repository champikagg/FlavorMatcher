import sqlite3
from sqlite3 import *
from lxml import etree 
import pymongo
from pymongo import MongoClient
import unicodedata
import nltk, re, pprint
import string
from nltk.corpus import stopwords
from string import punctuation
from string import maketrans
import requests
import urllib2
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
from pygeocoder import Geocoder
import tf_idf
import numpy as np
from operator import itemgetter, attrgetter
from geopy.distance import vincenty
from geopy.geocoders import GoogleV3
geolocator = GoogleV3()

regex = re.compile('[%s]' % re.escape(string.punctuation))
client = MongoClient
exclude = set(string.punctuation)
sw = set(stopwords.words('english'))
stemmer = nltk.PorterStemmer()

def clean_content(contents):
	content = " ".join(contents)
	content = content.split()
	return " ".join(content)
def any(seq):
	for s in seq:
		if s:
			return True
		return False

def findLocation(location):
	address, (latitude, longitude) = geolocator.geocode(location)
	return (latitude, longitude)
	
	
def findDistance(lat1, lon1, lat2, lon2):
	current = (lat1, lon1)
	new = (lat2, lon2)
	d=vincenty(current, new).miles
	return d

def compare_restaurants(rest,lat1,lon1,miles):
	con=connect("restinfo.db")
	c1=con.cursor()
	rest=rest.replace("'", "")
	review1=c1.execute("SELECT REVIEW FROM RESTAURANTS WHERE name like '%s' "%rest)

	for review in review1:
		r1=review[0]

	old_category=c1.execute("SELECT CATEGORY FROM RESTAURANTS WHERE name like '%s'"%rest) 	
	old_category=c1.fetchone()                                                                         
                                           
	for category_new in old_category: 
		c=category_new.lower()
	print c  

	comp=''
	rest_list=''
	comp_list=[]
	sort_before=[]	
	length=''

	category_match=c1.execute("SELECT NAME FROM RESTAURANTS WHERE CATEGORY like '%s'" %c)
	myqueryrecords = c1.fetchall()
	i=0
	length=len(myqueryrecords)
	while i<len(myqueryrecords):
		rest_match=myqueryrecords[i][0]
		print rest_match
		c1.execute("SELECT ADDRESS FROM RESTAURANTS WHERE NAME like '%s'" %rest_match)
		rest_address = c1.fetchone()
		rest_add=rest_address[0]
		print rest_add
		rest_match=rest_match.replace("'", "")
		lat2,lon2 = findLocation(rest_add)
		#print lat2, lon2
		rest_dist = findDistance(lat1, lon1, lat2, lon2)
		print rest_dist
		print miles
		if rest_dist < float(miles):
			print rest_match
			review2=c1.execute("SELECT REVIEW FROM RESTAURANTS WHERE NAME like '%s'" %rest_match)
			for review in review2:
				r2=review[0]	
			compare_rest=tf_idf.tf_idf(r1,r2)[0]
			comp_list.append(compare_rest[1])
			sort_before.append(myqueryrecords[i][0])
			comp=comp_list	
			rest_list=sort_before
		restaurants=[]	
		p=zip(comp,rest_list)
		x=sorted(p, key=itemgetter(0),reverse=True)
		i+=1
	c1.execute('DROP TABLE IF EXISTS RESTAURANTS_MATCH')
	con.commit()
	sql="""CREATE TABLE RESTAURANTS_MATCH (
			NAME  FLOAT,
			LATTITUDE FLOAT,
			LONGITUDE FLOAT,
			ADDRESS FLOAT
			)"""
	print x
	c1.execute(sql)
	
	for row in x:
		print row[1]
		restaurants=row[1].replace("'", "")
		y11=c1.execute("SELECT NAME, ADDRESS FROM RESTAURANTS WHERE NAME like '%s'" %restaurants)
		y=c1.fetchall()
		for y1 in y:
			latitude, longitude = findLocation(y1[1])
			print y1[0], latitude, longitude
			c1.execute("insert into RESTAURANTS_MATCH (name, lattitude,longitude,address) VALUES (?,?,?,?)",(y1[0],latitude,longitude,y1[1]))
			con.commit()
#compare_restaurants('hong hua','42.504939','-83.346878','10')

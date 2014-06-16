import MySQLdb
from lxml import etree 
#from __future__ import division
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

import getDistance
#from django.core.management import setup_environ
#from django.contrib.auth.models import User

#import settings
#from models import *

#setup_environ(settings)

regex = re.compile('[%s]' % re.escape(string.punctuation))
client = MongoClient
exclude = set(string.punctuation)
sw = set(stopwords.words('english'))
stemmer = nltk.PorterStemmer()
word_match=([
("japanese", "sushi bars"), 
("delis", "sandwiches"), 
("italian", "pizza"), 
("american (new)", "breakfast & brunch"), 
("american (traditional)", "breakfast & brunch"), 
("american (new)", "american (traditional)"), 
("american (new)", "bars"), 
("coffee & tea", "sandwiches"), 
("breakfast & brunch", "coffee & tea"), 
("breakfast & brunch", "diners"), 
("burgers", "fast food"), 
("american (new)", "italian"), 
("mediterranean", "middle Eastern"), 
("american (new)", "burgers"), 
("american (new)", "sandwiches"), 
("cafes", "coffee & tea"), 
("cafes", "sandwiches"), 
("american (new)", "french"), 
("breakfast & brunch", "cafes"), 
("american (new)", "seafood"), 
("american (traditional)", "burgers"), 
("breakfast & brunch", "sandwiches"), 
("indian", "pakistani"), 
("indian", "vegetarian"), 
("asian fusion", "japanese"), 
("american (traditional)", "diners"), 
("asian fusion", "chinese"), 
("salad", "sandwiches"), 
("caterers", "sandwiches"), 
("vegan", "vegetarian"), 
("american (new)", "wine bars"), 
("burgers", "sandwiches"), 
("greek", "mediterranean"), 
("breakfast & brunch", "burgers"), 
("breakfast & brunch", "french"), 
("american (new)", "mediterranean"), 
("american (new)", "lounges"), 
("food stands", "mexican"), 
("american (new)", "cafes"), 
("latin american", "mexican"), 
("breakfast & brunch", "mexican"), 
("barbeque", "korean"), 
("caterers", "delis"), 
("sandwiches", "vietnamese"), 
("asian fusion", "sushi bars"), 
("american (traditional)", "sandwiches"), 
("italian", "sandwiches"), 
("fast food", "mexican"), 
("middle eastern", "persian/iranian"), 
("seafood", "steakhouses"), 
("italian", "seafood"), 
("american (traditional)", "italian"), 
("american (new)", "pubs"), 
("american (new)", "coffee & tea"), 
("fish & chips", "seafood"), 
("cheesesteaks", "sandwiches"), 
("american (traditional)", "bars"), 
("american (new)", "pizza"), 
("breakfast & brunch", "creperies"), 
("american (new)", "vegetarian"), 
("french", "italian"), 
("italian", "wine Bars"), 
("american (New)", "gastropubs"), 
("mexican", "seafood"), 
("chinese", "taiwanese"), 
("bars", "mexican"), 
("pizza", "sandwiches"), 
("bakeries", "sandwiches"), 
("coffee & tea", "delis"), 
("bars", "breakfast & brunch"), 
("breakfast & brunch", "italian"), 
("chinese", "seafood"), 
("american (new)", "asian fusion"), 
("bakeries", "breakfast & brunch"), 
("american (new)", "delis"), 
("chinese", "japanese"), 
("cajun/creole", "seafood"), 
("american (new)", "mexican"), 
("american (new)", "salad"), 
("asian fusion", "thai"), 
("gluten-free", "pizza"), 
("barbeque", "caterers"), 
("bars", "italian"), 
("halal", "indian"), 
("chinese", "dim sum"), 
("american (traditional)", "pubs"), 
("caterers", "mexican"), 
("mediterranean", "turkish"), 
("burgers", "diners"), 
("cafes", "delis"), 
("chinese", "fast food"), 
("american (new)", "diners"), 
("american (traditional)", "seafood"), 
("grocery", "mexican"), 
("american (traditional)", "cafes"), 
("american (traditional)", "coffee & tea"), 
("bars", "lounges"), 
("american (traditional)", "french"), 
("chinese", "shanghainese"), 
("chinese", "thai"), 
("barbeque", "chinese")])



#c=c1.execute("SELECT NAME FROM RESTAURANTS ")

def clean_content(contents):
	content = " ".join(contents)
	content = content.split()
	return " ".join(content)
def any(seq):
	for s in seq:
		if s:
			return True
		return False
#for cs in c:
#	print clean_content(cs)
#print "Enter the restaurant name you wish you could go!",
#rest="hong hua"
#lat1=42.504939
#lon1=-83.346878
#"buddys pizza"
	#s for s in stringList if ("my string" in s)
#rest = raw_input()
#c11=c1.execute("SELECT NAME FROM RESTAURANTS")
#for names in c11:
#	print names
def compare_restaurants(rest,lat1,lon1,miles):
	con = MySQLdb.Connect(user='champika',host='localhost',passwd='mynewproject',db='restinfo')
	c1 = con.cursor()
	#c1.execute("SET global wait_timeout=30000000;")
	#c1.execute("SET session wait_timeout=30000000;")
	review11=c1.execute("SELECT REVIEW FROM RESTAURANTS WHERE name like %s ",(rest))
	review1=c1.fetchone()
	#print review1
	for review in review1:
		r1=review
	
		#print r1
	old_category1=c1.execute("SELECT CATEGORY FROM RESTAURANTS WHERE name like %s",(rest))
	old_category=c1.fetchone()
	c=[category_new for category_new in old_category]

	c=clean_content(c).lower()

#**************	
	rType1=[c]
	result_l = [ x[1] for x in word_match if x[0]==c]
	result_r = [ x[0] for x in word_match if x[1]==c]
	list= rType1+result_l+result_r
	comp_list=[]
	sort_before=[]
	length=''
	for results in list:
		print results
		category_match=c1.execute("SELECT NAME FROM RESTAURANTS WHERE CATEGORY like %s", (results))
		myqueryrecords = c1.fetchall()
		i=0
		length=len(myqueryrecords)
		while i<len(myqueryrecords):
			#print clean_content(myqueryrecords[i])
			rest_match=myqueryrecords[i]
			review22=c1.execute("SELECT REVIEW FROM RESTAURANTS WHERE NAME like %s", (rest_match))
			review2=c1.fetchall()
			for review in review2:
				r2=clean_content(review)	
			#print r1,r2
			compare_rest=tf_idf.tf_idf(r1,r2)[0]
			comp_list.append(compare_rest[1])
			sort_before.append(clean_content(myqueryrecords[i]))
			i+=1
		comp=comp_list	
		rest_list=sort_before
	restaurants=[]	
	p=zip(comp,rest_list)
	#print p
	x=sorted(p, key=itemgetter(0),reverse=True)
	#print x
	#rest_name=[row[1] for row in x]
	#rest_similar=[row[0] for row in x]
	#print rest_name, "   ", rest_similar
	#print sorted(rest_list, key=p.__getitem__)
	c1.execute('DROP TABLE IF EXISTS RESTAURANTS_MATCH')
	con.commit()
	sql="""CREATE TABLE `RESTAURANTS_MATCH` (
			NAME  TEXT,
			LATTITUDE TEXT,
			LONGITUDE TEXT
			)"""


	c1.execute(sql)
	
	for row in x:
		restaurants=row[1]
		y11=c1.execute("SELECT NAME, LONGITUDE, LATTITUDE FROM RESTAURANTS WHERE NAME like %s", (restaurants))
		y=c1.fetchall()
		for y1 in y:
			print y1[0]
			c1.execute("insert into RESTAURANTS_MATCH values (%s,%s,%s)",(y1[0],y1[1],y1[2]))
			con.commit()
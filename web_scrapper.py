#from __future__ import print_function
import MySQLdb
import warnings
from bs4 import BeautifulSoup 
import urllib2 


import htql
from lxml import etree 
import MySQLdb
 
from sqlite3 import * 
import nltk
import string
import re
import pymongo
from pymongo import MongoClient
from nltk.corpus import stopwords
con = MySQLdb.Connect(user='champika',host='localhost',passwd='mynewproject',db='restinfo')

c = con.cursor()

c.execute('DROP TABLE IF EXISTS RESTAURANTS')
con.commit()
c.execute("""CREATE TABLE `RESTAURANTS` (
			 NAME  TEXT,
			 DESCRIPTION TEXT,
			 TELEPHONE TEXT,
			 ADDRESS TEXT,
			 LATTITUDE TEXT,
			 LONGITUDE TEXT,
			 CATEGORY TEXT,
			 REVIEW TEXT,
			 PRICE TEXT,
			 RESERVATIONS TEXT,
			 DELIVERY TEXT,
			 TAKEOUT TEXT,
			 CREDITCARD TEXT,
			 GOODFOR TEXT,
			 PARKING TEXT,
			 WHEELCHAIR TEXT,
			 GOODFORKIDS TEXT,
			 GOODFORGROUPS TEXT,
			 ATTIRE TEXT,
			 AMBIENCE TEXT,
			 NOISELEVEL TEXT,
			 ALCOHOL TEXT,
			 OUTDOOR TEXT,
			 WIFI TEXT,
			 HASTV TEXT,
			 WAITERS TEXT,
			 CATERS TEXT) """)
		
		

#url="http://www.yelp.com/search?find_desc=dinner&find_loc=Farmington+Hills%2C+MI&ns=1"
def webscrapper(url):
	page=urllib2.urlopen(url) 
	soup = BeautifulSoup(page.read()) 

	restaurants=soup.findAll('a','biz-name') 

	for eachrestaurant in restaurants: 
		rest_url= "http://www.yelp.com"+ eachrestaurant['href']  
		org_url=urllib2.urlopen(rest_url) 
		soup1=BeautifulSoup(org_url.read()) 
	
		def get_address(spans, itemprop):
			address = ""
			addresses = [span.contents for span in spans if span.get("itemprop")==itemprop]
			if len(addresses)>0: 
				address = addresses[0][0]
			return address
		dts = soup1.findAll('dt')
	
		def get_price(dts, TextInfo):
			for dt in soup1.findAll('dt',{"attribute-key"}):
				info=dt.contents[0]
				textinfo=info
				dds = soup1.findAll('dd')
				for dd in dds:	
					content=dd.contents[0]
					rest_info=content.strip().lstrip("$")
					return rest_info	
	
		def get_moredetail(divs, TextInfo):
			
			dts=soup1.findAll('dt')
			rest_info_q= []
			for dt in dts:
				content=dt.contents[0]
				rest_info=content.strip()
				rest_info_q.append(rest_info)
	
			dds = soup1.findAll('dd')
			rest_info_a=[]
			for dd in dds:	
				content=dd.contents[0]
				rest_info=content.strip()
				rest_info_a.append(rest_info)
		#print rest_info_a
			p1=zip(reversed(rest_info_q),reversed(rest_info_a))
			q=[]
			a=[]
			for x,y in p1:
				q=x
				a=y
				if x==TextInfo:
					return y
			
	#div for div in divs_rest if div.get('class') and div['class']==["yelp-menu"]		

		def get_detail(detail):
		
			g_name=""
			g_description=""
			g_lattitude=""
			g_longitude=""
		
			rest_name=soup1.findAll('meta',{'property':'og:title'})
			rest_longitude=soup1.findAll('meta',{'property':'place:location:longitude'})
			rest_latitude=soup1.findAll('meta',{'property':'place:location:latitude'})
			rest_description=soup1.findAll('meta',{'property':'og:description'})
		
			if len(detail)>0:
				for eachrest_name in rest_name:
					g_name=eachrest_name['content']
				for eachrest_longitude in rest_longitude:
					g_longitude=eachrest_longitude['content']
				for eachrest_lattitude in rest_latitude:
					g_lattitude=eachrest_lattitude['content']
				for eachrest_description in rest_description:
					g_description=eachrest_description['content']
			
				
			return g_name, g_description,g_lattitude,g_longitude
		
		review_tag  = {'itemprop':re.compile("description")}

		all_reviews = soup1.findAll(attrs=review_tag)
		review_list=[]
		for text in all_reviews:
			if soup1.findAll('meta',{'content':'5.0'}):
				review= ''.join(text.findAll(text=True)).strip()
				review_list.append(review)
		review = review_list
		def clean_content(contents):
			content = " ".join(contents)
			content = content.split()
			return " ".join(content)
		
		newreview = clean_content(review).encode('ascii',errors='ignore')
	   	def remove_accents(input_str):
			new= ''.join( c for c in input_str if  c not in '?:!/;&#\@$%^*~",.<>(){}[]-=+' )
			new="".join(i for i in new if ord(i)<128)
			return new.lower()
		new_review=remove_accents(newreview)
		spans = soup1.findAll('span')
		dds = soup1.findAll('dd')	
	
		oldname, description, lattitude, longitude =get_detail('detail')
		name=remove_accents(oldname)
		telephone = get_address(spans, "telephone")
		street = get_address(spans, "streetAddress")
		city = get_address(spans, "addressLocality")
		state = get_address(spans, "addressRegion")
		zipcode = get_address(spans, "postalCode")

		price_range = get_price(dts,"Price Range")
		reservations = get_moredetail(dts,"Takes Reservations")
		delivery = get_moredetail(dts,"Delivery")
		takeout = get_moredetail(dts,"Take-out")
		creditCard = get_moredetail(dts,"Accepts Credit Cards")
		goodfor = get_moredetail(dts,"Good For")
		parking = get_moredetail(dts,"Parking")
		wheelchair = get_moredetail(dts,"Wheelchair Accessible")
		goodforKids = get_moredetail(dts,"Good for Kids")
		goodforGroups = get_moredetail(dts,"Good for Groups")
		attire = get_moredetail(dts,"Attire")
		ambience = get_moredetail(dts,"Ambience")
		noiselevel = get_moredetail(dts,"Noise Level")
		alcohol = get_moredetail(dts,"Alcohol")
		outdoor = get_moredetail(dts,"Outdoor Seating")
		wifi = get_moredetail(dts,"Wi-Fi")
		tv = get_moredetail(dts,"Has TV")
		waiter = get_moredetail(dts,"Waiter Service")
		caters = get_moredetail(dts,"Caters")
	
		
	
		category_tag  = {'itemprop':re.compile("child")}
		all_category = soup1.findAll(attrs=category_tag)
		category_list=[]
		for text in all_category:
			if soup1.findAll('span'):
				category= ''.join(text.findAll(text=True)).strip()
				category_list.append(category)
			
		categories = category_list
		category = clean_content(categories).encode('ascii',errors='ignore')
	
		street_address = street + ' ' + city + ', ' + state + ' ' + zipcode
		
		c.execute("INSERT INTO RESTAURANTS  (name,description, telephone, address, lattitude, longitude,category, review,price,reservations,delivery,takeout, creditCard, goodfor, parking, wheelchair, goodforKids, goodforGroups, attire, ambience,noiselevel, alcohol, outdoor, wifi, hastv, waiters, caters) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
			(name,description.lower(), telephone, street_address, lattitude,longitude, category, new_review, price_range, reservations, delivery, takeout,\
			creditCard, goodfor, parking, wheelchair, goodforKids, goodforGroups, attire, ambience, noiselevel,alcohol, outdoor,wifi, tv, waiter, caters))
		con.commit()
	c.execute("DELETE FROM RESTAURANTS WHERE name = ''	")
	c.execute("select name, description from RESTAURANTS")
	for row in c:
		print row
	
	c.close
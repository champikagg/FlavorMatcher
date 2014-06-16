import web_scrapper

#scraping data on first page
url="http://www.yelp.com/search?find_desc=restaurants&find_loc=Farmington+Hills%2C+MI&ns"
web_scrapper.webscrapper(url)
i=1
while i<10:
	url="http://www.yelp.com/search?find_desc=restaurants&find_loc=Farmington+Hills%2C+MI&start="+str(10*i)
	web_scrapper.webscrapper(url)
	i+=1
	

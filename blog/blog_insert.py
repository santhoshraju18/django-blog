import sys
import os
import json
import MySQLdb
import MySQLdb.cursors
import csv
from urlparse import parse_qs, urlparse
import urllib
import random
from datetime import date

db = MySQLdb.connect(host= "localhost",user="root",passwd="password",db="demo",cursorclass=MySQLdb.cursors.DictCursor)

cursor = db.cursor()

def get_data():
	json_data = {}
	category_data = []
	post_data = []
	
	# Category
	with open('/home/eskguptha/Downloads/aci.json') as data_file:
		json_data = json.load(data_file)
	for p,each_dict in enumerate(json_data):
		
		post_id = p+1
		image_url =  parse_qs(urlparse(each_dict['image_url']).query, keep_blank_values=True)
		category = each_dict['link'].split('/')[3]
		slug = "http://demo.revenuemantra.com/post/%s"%post_id
		each_dict.update({"url":slug, "image":image_url['n'][-1],"id":post_id,"categories":category,"vendor":"Autocar India","sku":post_id})
		del each_dict['image_url']
		del each_dict['link']
		post_data.append(each_dict)
		if category not in category_data:
			category_data.append(str(category))
	return post_data, category_data

def blog_insert():
	post_data, category_data = get_data()
	category_post_data = []
	category_data = tuple((i+1,each,'') for i, each in enumerate(category_data))


	query = "INSERT INTO blog_category VALUES (%s, %s,%s)"
	try:
		cursor.executemany(query, category_data)
		db.commit()
	except Exception as e:
		print e
		db.rollback()

	# Category Cache
	blog_category_cache = {}
	cursor.execute("SELECT * FROM blog_category ")
	blog_category_result = cursor.fetchall()
	for each in blog_category_result:
		blog_category_cache[each['name']] = each

	# Post
	post_values = tuple((each['post_id'], each['title'], 'auto Car', each['image_url'],'',each['link']) for j, each in enumerate(post_data))
	category_post_values = tuple((j+1, each['post_id'],  blog_category_cache.get(each['category'], '')['id']) for j, each in enumerate(post_data))
	query1 = "INSERT INTO blog_post VALUES (%s,%s,%s,%s, %s,%s)"
	query2 = "INSERT INTO blog_post_category VALUES (%s,%s,%s)"
	try:
		cursor.executemany(query1, post_values)
		cursor.executemany(query2, category_post_values)
		db.commit()
	except Exception as e:
		print e
		db.rollback()

	return True



def blog_to_json():
	post_data, category_data = get_data()
	with open('autocar_catalog.json', 'w') as outfile:
	    json.dump(post_data, outfile,indent=4)
    	outfile.close()


def download_images():
	#urllib.urlretrieve("http://www.gunnerkrigg.com//comics/00000001.jpg", "00000001.jpg")

	keywords = [u'Although', u'the', u'Linea', u'has', u'been', u'around', u'for', u'a', u'very', u'long', u'time,', u'it', u'has', u'always', u'remained', u'on', u'the', u'sidelines', u'of', u'the', u'market.', u'This', u'had', u'more', u'to', u'do', u'with', u'the', u'brand', u'rather', u'than', u'the', u'product', u'itself.', u'The', u'current', u'car', u'is', u'the', u'same', u'generation', u'car', u'as', u'was', u'launched', u'back', u'in', u'2009,', u'but', u'it', u'has', u'gone', u'through', u'various', u'updates', u'and', u'facelifts', u'through', u'the', u'years.', u'This', u'time', u'round', u'there\u2019s', u'a', u'more', u'powerful', u'T-Jet', u'engine', u'and', u'a', u'handy', u'touchscreen', u'infotainment', u'system.', u'We', u'wish', u'though', u'that', u'Fiat', u'had', u'done', u'more', u'to', u'differentiate', u'the', u'125', u'S', u'from', u'the', u'regular', u'Linea,', u'apart', u'from', u'just', u'some', u'badging', u'at', u'the', u'rear', u'and', u'A-pillars.', u'We', u'can', u'expect', u'quite', u'a', u'few', u'enthusiasts', u'looking', u'for', u'some', u'visual', u'mods', u'for', u'their', u'cars.']
	with open('../initial_authors.json') as data_file:    
		authors = json.load(data_file)

	print authors

	with open('../initial_articles.json') as data_file:    
		articles = json.load(data_file)
		for article in  articles:
			if article["fields"].get("image"):
				article["fields"]["image"] = str(article["pk"])+".jpg"
			author = random.choice(authors)
			article["fields"]["author"] = author.get("pk")
			start_date = date.today().replace(day=1, month=1).toordinal()
			end_date = date.today().toordinal()
			random_day = date.fromordinal(random.randint(start_date, end_date))
			article["fields"]["published_date"] = random_day.strftime("%Y-%m-%d %H:%M:%S")
			article["fields"]["description"] = ' '.join(keywords[random.randint(0,len(keywords)):]).title()
			del article["fields"]["slug"]

	with open('../blog_articles.json', 'w') as outfile:
	    json.dump(articles, outfile, indent=4)
    	outfile.close()
	#urllib.urlretrieve(article["fields"].get("image"), "../media/articles/"+str(article["pk"])+".jpg")

if __name__=="__main__":
	#blog_insert()
	#catalog_insert()
	download_images()
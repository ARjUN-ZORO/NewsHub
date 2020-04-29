from newshub.data.settings import *
from bs4 import BeautifulSoup
import requests
import re
import datetime
import pytz
from flask import jsonify
from pymongo import MongoClient
import pymongo


def scrape():
	errors = {}
	errors["link_errors"] = {}
	link_errors = errors["link_errors"]
	link_errors["link_error"] = []
	link_error = link_errors["link_error"]
	errors["page_errors"] = {}
	page_errors = errors["page_errors"]
	page_errors["page_error"] = []
	page_error = page_errors["page_error"]
	link_data = {}
	page_d = {}
	date = datetime.datetime.now(pytz.timezone('Asia/Calcutta')).strftime('%x')
	try:
		client1 = MongoClient(DB_CON)
		db1 = client1.newshub
		doc1 = db1["links"]
	except Exception as e:
		link_error.append({'error': e, 'time': datetime.datetime.now(pytz.timezone('Asia/Calcutta'))})

	try:
		client2 = MongoClient(DB_CON)
		db2 = client2.newshub
		doc2 = db2["page_data"]
	except Exception as e:
		page_error.append({'error': e, 'time': datetime.datetime.now(pytz.timezone('Asia/Calcutta'))})

	request_page = requests.get(
		url=SCRAPE)
	raw_content = request_page.content
	html_page = BeautifulSoup(raw_content, "html.parser")
	latest_news_ul = html_page.find_all("ul", {"class": "latest-news"})
	latest_news_ul = latest_news_ul[0]
	li = latest_news_ul.find_all("li")
	li = li[::-1]
	links = []
	for all in li:
		link = all.find("a")['href']
		if doc1.find_one(link.split('/')[-1][:-4]):
			print('skip')
			pass
		else:
			try:
				link_data = {
					"_id": link.split('/')[-1][:-4],
					"link": link,
					"title": all.find("a").text,
					"time": all.find("span", {"class": "l-datetime"}).text,
					"type": all.find("span", {"class": "homeSection-name"}).text,
					"date": datetime.datetime.now(pytz.timezone('Asia/Calcutta')).strftime('%x')
				}
				res = doc1.insert_one(link_data)
				print(res.acknowledged)
				if (res.acknowledged):
					source = {'name': 'thehindu.com'}
					description = ''
					section_name = ''
					title = ''
					author_name = ''
					place = ''
					post_time = ''
					updated_time = ''
					img_name = ''
					img = ''
					content = ''
					url = ''
					try:
						_id = link.split('/')[-1][:-4]
						page = requests.get(url=link)
						contents = page.content
						soup = BeautifulSoup(contents, "html.parser")
						article_full = soup.find_all(
							"div", {"class": "article", "role": "main"})
						section_name = article_full[0].find(
							"a", {"class": 'section-name'}).text
						if (article_full[0].find("h1").text):
							title = article_full[0].find("h1").text
						if (article_full[0].find("a", {"class": 'auth-nm'})):
							author_name = article_full[0].find(
								"a", {"class": 'auth-nm'}).text
						place_time_uptime = article_full[0].find(
							"div", {"class": 'ut-container'})
						place = place_time_uptime.find_all(
							"span")[0].text.replace("\n", "")[:-2]
						post_time = place_time_uptime.find_all(
							"span")[1].text.replace("\n", "")
						# if (place_time_uptime.find_all("span")[2] is not None):
						#     updated_time=place_time_uptime.find_all("span")[2].text.replace("\n","")
						if (article_full[0].find_all("img", {"class": 'lead-img'})):
							img = article_full[0].find_all(
								"img", {"class": 'lead-img'})
							if (article_full[0].find_all("picture")):
								img = article_full[0].find_all("picture")
								if (img[0].find_all("source")[0]['srcset']):
									img = img[0].find_all("source")[
										0]['srcset']
									img_name = img.split('/')[-1]+".jpg"
									# if ('newshub/img/'+img_name):
									# 	pass
									# else:
									# 	with open('newshub/img/'+img_name ,'wb') as w:
									# 		img_res = requests.get(img,stream=True)
									# 		if not img_res.ok:
									# 			print(img_res)
									# 		for b in img_res.iter_content(1024):
									# 			if not b:
									# 				break
									# 			w.write(b)
						if (article_full[0].find("h2", {"class": 'intro'})):
							description = article_full[0].find(
								"h2", {"class": 'intro'}).text
						id_ = re.compile('^content-body-')
						content = article_full[0].find_all(
							"div", {"id": id_})[0].text
					except Exception as e:
						traceback.print_exc()
						print(e)
						page_error.append({'error': e, 'time': datetime.datetime.now(pytz.timezone('Asia/Calcutta'))})
					try:
						page_d = {
							'article_id': _id,
							'source': source,
							'section_name': section_name,
							'title': title,
							'author_name': author_name,
							'place': place,
							'post_time': post_time,
							# 'Updated':updated_time,
							'img_name': img_name,
							'img_url': img,
							'description': description,
							'content': content,
							'url': link,
							'Comments': {}
						}
						doc2.insert_one(page_d)
					except Exception as e:
						page_error.append({'error': e, 'time': datetime.datetime.now(pytz.timezone('Asia/Calcutta'))})
						# time.sleep(34)


			except pymongo.errors.DuplicateKeyError:
				pass
			except Exception as er:
				link_error.append({'error': er, 'time': datetime.datetime.now(pytz.timezone('Asia/Calcutta'))})
			links.append(link)

	# last = doc.find({'date': datetime.datetime.now().strftime("%x")}).sort(
		# "time", pymongo.DESCENDING)[0]
	final = {'data': {'link_data': link_data, 'page_data': page_d}}
	all_data = {'errors': errors, 'final': final}
	# print(all_data)
	print(all_data)
	return all_data


# print(scrape())

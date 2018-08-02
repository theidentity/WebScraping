from bs4 import BeautifulSoup
import pandas as pd
import requests
import pickle
import os


def get_urls(url,num_pages=3):
	
	urls = []
	start,end = url.split('Reviews-')
	urls.append(start+end)
	num = 10
	for page in range(num_pages-1):
		urls.append(start+'or'+str(num)+'-'+end)
		num+=10

	print(urls)
	return urls

def get_page(url):

	page = requests.get(url)	
	return page

def get_by_class_name(soup,class_name,tag='div',mode='all'):
	if mode=='all':
		items = soup.findAll(tag,{'class':class_name})
	elif mode=='one':
		items = soup.find(tag,{'class':class_name})
	return items

def parse_review_components(soup,class_name,tag='div',mode='text'):
	if mode=='text':
		try:
			component = get_by_class_name(soup,class_name,tag,mode='one').text
			return component
		except:
			return ''

	if mode=='rating':
		try:
			rating = get_by_class_name(soup,class_name,tag,mode='one')['class'][-1]
			rating = int(rating.split('_')[-1])*5/100
			return rating
		except:
			return 2.5

def parse_review(review):
	
	review_dict = {}
	soup = BeautifulSoup(str(review),'html.parser')

	review_dict['review_title'] = parse_review_components(soup,'quote')
	review_dict['review_text'] = parse_review_components(soup,'entry')
	review_dict['username'] = parse_review_components(soup,'username')
	review_dict['location'] = parse_review_components(soup,'location')
	review_dict['rating'] = parse_review_components(soup,'ui_bubble_rating',tag='span',mode='rating')
	return review_dict

def display_review(parsed_review):

	print('\n____________________REVIEW____________________')
	print('Review Title\t:\t',parsed_review['review_title'])
	print('Review Text\t:\t',parsed_review['review_text'])
	print('Username\t:\t',parsed_review['username'])
	print('Location\t:\t',parsed_review['location'])
	print('Rating\t:\t',parsed_review['rating'])
	print('________________________________________________\n')


def append_review(review,title):
	
	filename = 'data/'+title+'.csv'

	review_df = pd.DataFrame()
	review_df.set_value(0,'Review Title',review['review_title'])
	review_df.set_value(0,'Review Text',review['review_text'])
	review_df.set_value(0,'Username',review['username'])
	review_df.set_value(0,'Location',review['location'])
	review_df.set_value(0,'Rating',review['rating'])

	if not os.path.isfile(filename):
		df = review_df
		df.to_csv(filename,index=False)
	else:
		df = pd.read_csv(filename)
		df = df.append(review_df)
		df.to_csv(filename,index=False)

def parse_page(page):
	soup = BeautifulSoup(page.text,'html.parser')
	title = get_by_class_name(soup,'heading_title',tag='h1',mode='one').text
	reviews = get_by_class_name(soup,'review-container')
	for review in reviews:
		parsed_review = parse_review(review)
		display_review(parsed_review)
		append_review(parsed_review,title)

if __name__ == '__main__':
	base_url = 'https://www.tripadvisor.com.sg/Attraction_Review-g294264-d2439664-Reviews-Universal_Studios_Singapore-Sentosa_Island.html'
	urls = get_urls(base_url,num_pages=2)

	for url in urls:
		page = get_page(url)
		parse_page(page)

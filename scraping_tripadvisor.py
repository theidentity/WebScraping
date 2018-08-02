from bs4 import BeautifulSoup
import pandas as pd
import requests
import pickle 


def get_page(url):
	# page = requests.get(url)
	# file = open('data/univ_studios.pkl','wb')
	# pickle.dump(page,file)

	file = open('data/univ_studios.pkl','rb')
	page = pickle.load(file)
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

def parse_page(page):
	soup = BeautifulSoup(page.text,'html.parser')
	reviews = get_by_class_name(soup,'review-container')
	for review in reviews:
		parsed_review = parse_review(review)
		display_review(parsed_review)


if __name__ == '__main__':
	url = 'https://www.tripadvisor.com.sg/Attraction_Review-g294264-d2439664-Reviews-Universal_Studios_Singapore-Sentosa_Island.html'
	page = get_page(url)
	# print(page.status_code)
	parse_page(page)

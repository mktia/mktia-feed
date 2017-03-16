# -*- coding:utf-8 -*-
import ast
import feedparser
import os
import tweepy
import urllib2

consumer_key = os.environ['ck']
consumer_secret = os.environ['cs']
access_token = os.environ['at']
access_token_secret = os.environ['as']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

feed_url_all = 'http://mikuta.main.jp/feed/data.html'
data = {}

def check_post(url, list_name):
	res = feedparser.parse(url)
	title = res.entries[0].title
	link = res.entries[0].link
	list = api.get_list(owner_screen_name='_mktia', slug=list_name)
	print('description: ' + list.description)
	print(link)
	if link != list.description:
		api.update_status(title + '\n' + link)
		api.update_list(slug=list_name, description=link, owner_screen_name='_mktia')
		print('Posted.')
	else:
		print(list_name + ' is not updated.')
	
			
if __name__ == '__main__':
	data = urllib2.urlopen(feed_url_all).read()
	data = ast.literal_eval(data)
	for i in range(len(data['site'])):
		print(data['site'][i], data['list'][i])
		check_post(data['site'][i], data['list'][i])
	
	print('---------- finished! ----------')
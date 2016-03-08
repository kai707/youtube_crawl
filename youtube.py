#coding:utf-8
#file:youtube.py

import sys
import requests
from BeautifulSoup import *
import urllib
import HTMLParser
import ast #conver str to dict
import argparse

def query(keyword, number, page):
	if type(number) == list:
		number = number[0]
	if type(page) == list:
		page = page[0]
	fixed = urllib.quote_plus(keyword)
	domain = "https://www.youtube.com"
	query = "/results?search_query="
	res = requests.get(domain + query + fixed + '&page=' + str(page))
	print domain + query + fixed + '&page=' + str(page)
	reshtml = BeautifulSoup(res.text)
	htmlparse = HTMLParser.HTMLParser()
	for each in reshtml.findAll('div',{'class':'yt-lockup-content'}):
		if '/user/' not in each.a['href']:
			print '%s ( %s )'% (htmlparse.unescape(each.a.text), getshort(domain + each.a['href']))
			des = each.findAll('div',{'dir':'ltr'})
			if des:
				print htmlparse.unescape(des[0].getText(' '))
			print getsentiment(domain + each.a['href'])
			print '\n\n'
			number = number-1
			if number == 0:
				break

def getsentiment(url):
	youtube = requests.get(url)
	youtubehtml = BeautifulSoup(youtube.text)
	try:
		likes = youtubehtml.findAll('button',{'title':u'我喜歡'})[0].findChild().text
	except:
		likes = ''
	try:
		dislikes = youtubehtml.findAll('button',{'title':u'我不喜歡'})[0].findChild().text
	except:
		dislikes = ''
	return 'like:%s\tdislike:%s' % (likes, dislikes)
	
def getshort(url):
	returnshort = 'https://url.fit/'
	en = urllib.quote_plus(url)
	shortenurl = 'https://developer.url.fit/api/shorten?long_url='
	s = urllib.urlopen(shortenurl+en)
	try:
		msgdic = ast.literal_eval(s.read())
	except:
		msgdic = ''
	return  returnshort + msgdic['url'] if 'url' in msgdic else url

parser = argparse.ArgumentParser(description='Crawl the search results of Youtube')
parser.add_argument('-n', dest='number', nargs=1, \
					help='number of search result. default is 5', type=int,default=5)
parser.add_argument('-p', dest='page', nargs=1, help='page that you parse. default is 1',\
					type=int, default=1)
parser.add_argument('keyword', help='search keyword', metavar='keyword', type=str)
args = parser.parse_args()
query(sys.argv[1], args.number, args.page)

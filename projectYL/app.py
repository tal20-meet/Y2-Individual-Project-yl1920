from flask import Flask, request, redirect,g, url_for, render_template
from flask import session as login_session
import os, requests, json
import urllib as urllibparse
import base64
from urlparse import urlparse
from databases import *
app = Flask(__name__)

@app.route('/')
def quote():
	def extract_urls(text):
	    out = []
	    for word in text.split(' '):
	        thing = urlparse(word.strip())
	        if thing.scheme:
	            out.append(word)
	    return out
	headers= {'Accept': 'application/hal+json'}
	response = requests.get("https://tronalddump.io/random/quote", headers=headers)
	parsed_content = json.loads(response.content)
	quote = parsed_content["value"]
	quote1 = quote
	org_url = parsed_content["_embedded"]["source"][0]["url"]
	org_url1=org_url
	#quote += " https://twitter.com/realDonaldTrump/status/770330631783972868 "
	link = ''
	media = ''
	hashtags = []
	ht = ''
	after_ht = False
	hashtag = ''
	
	if extract_urls(quote)!=[]:
	 	link = extract_urls(quote)[0]
	if (link[:27]=="https://twitter.com/i/status" or link[:26]=='https://pbs.twimg.com/media'):
		media = link
	for i in quote:
		if after_ht == True:
			ht += i

		if i=='#':
			after_ht = True
		elif i==' ':
			after_ht = False
			hashtags.append(ht)
			ht=''
	if (hashtags!=[]):
		hashtag = hashtags[0]
	org_url
	hashtag1=hashtag

	if(hashtag1!='' and media!=''):
		add_quote(quote1, hashtag1, media, org_url)
	elif(hashtag1=='' and media!=''):
		add_quote(quote1, ' ', media, org_url)
	elif(hashtag1!='' and media==''):
		add_quote(quote1, hashtag1, ' ', org_url)
	else:
		add_quote(quote1, ' ', ' ', org_url)

	return render_template("index.html", quote=quote, org_url=org_url, media=media, hashtag=hashtag)

@app.route('/history')
def history():
	print_all()
	quotes_parsed = query_all()
	quotes =[]
	links = []
	hashtags = []
	media = []
	hashtag_links = []
	for i in quotes_parsed:
		quotes.append(i.quote)
		links.append(i.link)
		hashtags.append(i.hashtag)
		media.append(i.media)
		hashtag_links.append("https://twitter.com/hashtag/"+i.hashtag+"?src=hash")
	
	if len(links)!=1 and len(links)!=2:
		if (len(links)%2==0):
			quotes_len = int(len(links)/2)
		else:
			quotes_len = int(len(links)/2)+1
	elif len(links)==2:
		quotes_len=1
	else:
		quotes_len = 0

	return render_template("results.html",quotes=quotes,links=links, hashtags=hashtags, media=media, hashtag_links=hashtag_links, quotes_len=quotes_len)

@app.route('/del_quotes')
def del_quotes():
	del_all_quotes()
	quotes_parsed = query_all()
	quotes =[]
	links = []
	hashtags = []
	media = []
	hashtag_links = []
	for i in quotes_parsed:
		quotes.append(i.quote)
		links.append(i.link)
		hashtags.append(i.hashtag)
		media.append(i.media)
		hashtag_links.append("https://twitter.com/hashtag/"+i.hashtag+"?src=hash")
	
	if len(links)!=1 and len(links)!=2:
		if (len(links)%2==0):
			quotes_len = int(len(links)/2)
		else:
			quotes_len = int(len(links)/2)+1
	elif len(links)==2:
		quotes_len=1
	else:
		quotes_len = 0

	return render_template("results.html",quotes=quotes,links=links, hashtags=hashtags, media=media, hashtag_links=hashtag_links, quotes_len=quotes_len)




if __name__ == '__main__':
    app.run(debug=True)
   
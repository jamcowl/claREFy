#! /usr/bin/env python

import re
import keyPhrasesMSCS as kp
import urllib, urllib2
#import xml.etree.ElementTree as ET
import feedparser
import wikipedia




# get intro from wikipedia for a topic
def getWikiIntro(inString):
	out = "FAILFAIL"	
	try:
		out = wikipedia.summary(inString, sentences=4)
	except Exception, e:
		pass
	return out

# get info from arxiv
def infoFromArXivOLD(arXivCode):
	url = 'http://export.arxiv.org/api/query?search_query=all:'+str(arXivCode)
	data = urllib.urlopen(url).read()
	feed = feedparser.parse(data)
	for item in feed.entries:
		print item
	print data
	title = data.split("title>")[2][:-2].strip().replace("\n"," ").replace("   "," ").replace("  "," ")
	print "\n\n\ntitle:\n"+title
	summary = data.split("summary>")[1][:-2].strip().replace("\n"," ").replace("   "," ").replace("  "," ")
	print "\n\n\nsummary:\n"+summary
	return [title,summary]


def infoFromArXiv(arXivCode):
	url = "https://arxiv.org/abs/"+str(arXivCode)
	pagesource = urllib2.urlopen(url)
	title = ""
	abstract = ""
	summary = ""
	onTitle = False
	onSummary = False
	for line in pagesource:
		if line.strip().startswith("<title>"):
			onTitle = True
		if onTitle:
			title = title+line
		if line.strip().endswith("</title>"):
			onTitle = False
		if '<span class="descriptor">Abstract:</span>' in line:
			onSummary = True
		if onSummary:
			summary = summary+line.strip('"<span class="descriptor">Abstract:</span> "')
		if "</blockquote>" in line:
			onSummary = False
			break
	title = title.strip().replace("<title>","").replace("</title>","").replace("\n"," ").replace("   "," ").replace("  "," ")
	return [title,summary]
		

def getTopPhrases(longString):
	allkeywords = kp.getKeyWords(longString)
	top = []
	for keyword in allkeywords:
		keystr = str(keyword)
		if len(keystr.split()) > 1:
			top.append(keystr)
	return top




# get PDF url from arxiv-looking string
def arXivPDF(someString):

	# find arxiv code
	arXivCode = re.findall(r'(\d{4}.\d{4})', someString)
	if len(arXivCode) != 1:
		return "FAIL: Couldn't obtain arXiv code."
	code = arXivCode[0]
	pdfurl = "https://arXiv.org/pdf/"+code+".pdf"
	return pdfurl

# get PDF url from arxiv-looking string
def findArXivCode(someString):

	# find arxiv code
	arXivCode = re.findall(r'(\d{4}.\d{4})', someString)
	if len(arXivCode) != 1:
		return "FAIL: Couldn't obtain arXiv code."
	code = arXivCode[0]
	return code

# rank citations by importance
def rankCitations(unrankedCitations):
	rankedCitations = []
	# TODO
	return rankedCitations

# make an HTML card to display citation
def getHTMLcitationCard(citationString):
	citationCard = ""
	# TODO
	return citationCard

# get definitions of key phrases
def definePhrase(somePhrase):
	definition = ""
	# TODO
	return  definition

# make an HTML card to display key phrase and definitio
def getHTMLphraseCard(somePhrase,phraseDefinition):
	phraseCard = ""
	# TODO
	return phraseCard




# the mother function
def getFullPageHTML(userInput):

	# get data from arXiv
	code = findArXivCode(userInput)
	[paperTitle, paperAbstract] = infoFromArXiv(code)
	print "GOT TITLE: "+paperTitle
	print "GOT ABSTRACT: "+paperAbstract
	keyps = getTopPhrases(paperAbstract)
	
	# build content
	content = "" # construct decent looking body (without going to the gym)
	for keyp in keyps:
		description = getWikiIntro(keyp)
		if description != "FAILFAIL":
			content=content+"\n\n"+(keyp+":\n"+getWikiIntro(keyp)+"\n-------------------")
	
	# constant style things
	topOfPage = """<!DOCTYPE html><html lang="en"><head><title>"""+paperTitle+"""</title><link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet"><link href="http://getbootstrap.com/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet"><link href="/static/newindex.css" rel="stylesheet"><script src="/static/js/jquery-1.11.2.js"></script><script src="/static/js/signUp.js"></script></head><body><div class="container"><div class="header"><h3 class="text-muted">clarefy</h3></div><div class="jumbotron"><div align="center"><img src="/static/images/clarefy_logo.png" align="middle"></div><h1>""" # everything up to a header
	header = paperTitle+"</h1><p>" # set page title from paper title
	
	bottomOfPage = """</p></div><p>Powered by:</p><p></p><a href="https://azure.microsoft.com/en-gb/services/cognitive-services/"><img src="/static/images/mscs.png" style="width:278px;height:83px;"><a href="https://scholar.google.co.uk/"><img src="/static/images/google_scholar.png" style="width:217px;height:83px;"><a href="https://aws.amazon.com"><img src="/static/images/aws_logo.png" style="width:189px;height:83px;"> <a href="http://flask.pocoo.org/"><img src="/static/images/flask.png" style="width:212px;height:83px;"> </a><footer class="footer"><p></p><p>&copy; clarefy 2017</p></footer>"""
	return topOfPage+header+content+bottomOfPage






"""

[testTitle, testSummary] = infoFromArXiv(1412.1633)
keyps = getTopPhrases(testSummary)
for keyp in keyps:
	print keyp+":\n"+getWikiIntro(keyp)+"\n-------------------"

"""




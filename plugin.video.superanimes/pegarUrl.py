#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup


class abrir_url(object):
	def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='',
				 timeout='10'):
		if not proxy == None:
			proxy_handler = urllib2.ProxyHandler({'http': '%s' % (proxy)})
			opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
			opener = urllib2.install_opener(opener)
		if output == 'cookie' or not close == True:
			import cookielib

			cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
			opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
			opener = urllib2.install_opener(opener)
		if not post == None:
			request = urllib2.Request(url, post)
		else:
			request = urllib2.Request(url, None)
		if mobile == True:
			request.add_header('User-Agent',
							   'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
		else:
			request.add_header('User-Agent',
							   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
		if not referer == None:
			request.add_header('Referer', referer)
		if not cookie == None:
			request.add_header('cookie', cookie)
		response = urllib2.urlopen(request, timeout=int(timeout))
		if output == 'cookie':
			result = str(response.headers.get('Set-Cookie'))
		elif output == 'geturl':
			result = response.geturl()
		else:
			result = response.read()
		if close == True:
			response.close()
		self.result = result


url = "http://www.superanimes.com/dragon-ball-super/episodio-11#"

codigo_fonte = abrir_url(url).result
soup = BeautifulSoup(codigo_fonte)
baixar = str(soup.find('div', class_='selectVideo'))
burl = str(re.findall(r'<a href="(.+?)" title=".+?">', baixar))
burl = burl.replace("['","").replace("']","")

codigo2 = abrir_url(burl).result
soup2 = BeautifulSoup(codigo2).prettify()
vurl = str(re.findall(r'<link href="(.+?)" itemprop="embedURL">', soup2))
vurl = vurl.replace("[u'","").replace("']","")
print vurl





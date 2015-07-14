#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2013 A minha casa digital
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# gutoakashi1   01/07/2015


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib
import urllib2
import re
import xbmcplugin
import xbmcgui
import xbmc
import xbmcaddon
from bs4 import BeautifulSoup

versao = '0.1.0'
addon_id = 'plugin.video.superanimes'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'


##############################MENUS###################################

def CATEGORIES():
	dialog = xbmcgui.Dialog()
	dialog.ok("Atualizado", "Addon atualizado por gutoakashi1. email: akx.kodi@bol.com.br")
	dialog = xbmcgui.Dialog()
	dialog.ok("Doações",
			  "Faça sua doação para manter o addon sempre atualizado. Mande um email para akx.kodi@bol.com.br para mais informações")
	addDir('LISTA', 'http://www.superanimes.com/lista', 1, artfolder + 'categorias.png')
	addDir('DUBLADOS', 'http://www.superanimes.com/dublado', 1, artfolder + 'destaques.png')
	addDir('LEGENDADOS', 'http://www.superanimes.com/legendado', 1, artfolder + 'destaques.png')
	addDir('LANÇAMENTOS', 'http://www.superanimes.com/lancamento', 6, artfolder + 'destaques.png')

#############################FUNCOES##################################

def listar_animes(url):
	codigo_fonte = abrir_url(url).result
	soup = BeautifulSoup(codigo_fonte)
	miniaturas = str(soup.find_all('div', class_='boxLista2Img'))
	match = re.compile(r'<a href="(.+?)" title="(.+?)">').findall(miniaturas)
	img = re.compile(r'<img alt=".+?" src="(.+?)" title=".+?"/>').findall(miniaturas)

	a = []
	for x in range(0, len(match)):
		temp = [match[x][0], match[x][1], img[x]]
		a.append(temp)

	total = len(a)
	for url2, titulo, img in a:
		addDir(titulo, url2, 4, img, True, total)

	try:
		n = re.search(r'http://www.superanimes.com/.+?\?letra=.*?&pagina=(.?)', url).group(1)
	except:
		url = url + '&pagina=1'
		n = 1

	n = int(n)
	m = n+1
	prox_pag = url.replace(str(n), str(m))
	addDir('Proxima Pagina >>>', prox_pag, 3, artfolder + 'destaques.png')

def listar_lancamentos(url):
	codigo_fonte = abrir_url(url).result
	soup = BeautifulSoup(codigo_fonte)
	miniaturas = str(soup.find_all('div', class_='lancamentoBoxNome'))
	match = re.compile(r'<a href="(.+?)" style=".*?" title="(.+?)">').findall(miniaturas)
	img = re.compile(r'<img height=".*?" src="(.+?)" style=".*?" width=".*?">').findall(miniaturas)

	a = []
	for x in range(0, len(match)):
		temp = [match[x][0], match[x][1], img[x]]
		a.append(temp)

	total = len(a)
	for url2, titulo, img in a:
		addDir(titulo, url2, 4, img, True, total)

	try:
		n = re.search(r'http://www.superanimes.com/.+?\?&pagina=(.?)', url).group(1)
	except:
		url = url + '?&pagina=1'
		n = 1

	n = int(n)
	m = n+1
	prox_pag = url.replace(str(n), str(m))
	addDir('Proxima Pagina >>>', prox_pag, 6, artfolder + 'destaques.png')

'''
def listar_filmes(url):
	codigo_fonte = abrir_url(url).result
	soup = BeautifulSoup(codigo_fonte)
	miniaturas = str(soup.find_all('div', class_='boxLista2Filme'))
	print miniaturas
	match = re.compile(r'<a href="(.+?)" title="(.+?)">').findall(miniaturas)
	img = re.compile(r'<img alt=".*?" height=".*?" src="(.+?)" title=".*?" width=".*?"/>').findall(miniaturas)

	a = []
	for x in range(0, len(match)):
		temp = [match[x][0], match[x][1], img[x]]
		a.append(temp)

	total = len(a)
	for url2, titulo, img in a:
		addDir(titulo, url2, 8, img, True, total)

	try:
		n = re.search(r'http://www.superanimes.com/.+?\?&pagina=(.?)', url).group(1)
	except:
		url = url + '?&pagina=1'
		n = 1

	n = int(n)
	m = n+1
	prox_pag = url.replace(str(n), str(m))
	addDir('Proxima Pagina >>>', prox_pag, 7, artfolder + 'destaques.png')
'''

def montar_url(url, name):
	url = url + '?letra=%s' % name
	listar_animes(url)


def listar_animes2(url):
	codigo_fonte = abrir_url(url).result
	soup = BeautifulSoup(codigo_fonte)
	miniaturas = str(soup.find_all('div', class_='epsBoxImg'))
	match = re.compile(r'<a href="(.+?)" title="(.+?)">').findall(miniaturas)
	img = re.compile(r'<img alt=".+?" src="(.+?)" title=".+?"/>').findall(miniaturas)

	a = []
	for x in range(0, len(match)):
		temp = [match[x][0], match[x][1], img[x]]
		a.append(temp)

	total = len(a)
	for url2, titulo, img in a:
		addDir(titulo, url2, 5, img, False, total)

	try:
		n = re.search(r'http://www.superanimes.com/.+?\?&pagina=(.?)', url).group(1)
	except:
		url = url + '?&pagina=1'
		n = 1

	n = int(n)
	m = n+1

	prox_pag = url.replace(str(n), str(m))

	print prox_pag
	addDir('Proxima Pagina >>>', prox_pag, 4, artfolder + 'destaques.png')

def letras(url):
	addDir('#', url, 2, artfolder + 'zero.jpg')
	addDir('A', url, 2, artfolder + 'a.jpg')
	addDir('B', url, 2, artfolder + 'b.jpg')
	addDir('C', url, 2, artfolder + 'c.jpg')
	addDir('D', url, 2, artfolder + 'd.jpg')
	addDir('E', url, 2, artfolder + 'e.jpg')
	addDir('F', url, 2, artfolder + 'f.jpg')
	addDir('G', url, 2, artfolder + 'g.jpg')
	addDir('H', url, 2, artfolder + 'h.jpg')
	addDir('I', url, 2, artfolder + 'i.jpg')
	addDir('J', url, 2, artfolder + 'j.jpg')
	addDir('K', url, 2, artfolder + 'k.jpg')
	addDir('L', url, 2, artfolder + 'l.jpg')
	addDir('M', url, 2, artfolder + 'm.jpg')
	addDir('N', url, 2, artfolder + 'n.jpg')
	addDir('O', url, 2, artfolder + 'o.jpg')
	addDir('P', url, 2, artfolder + 'p.jpg')
	addDir('Q', url, 2, artfolder + 'q.jpg')
	addDir('R', url, 2, artfolder + 'r.jpg')
	addDir('S', url, 2, artfolder + 's.jpg')
	addDir('T', url, 2, artfolder + 't.jpg')
	addDir('U', url, 2, artfolder + 'u.jpg')
	addDir('V', url, 2, artfolder + 'v.jpg')
	addDir('W', url, 2, artfolder + 'w.jpg')
	addDir('X', url, 2, artfolder + 'x.jpg')
	addDir('Y', url, 2, artfolder + 'y.jpg')
	addDir('Z', url, 2, artfolder + 'z.jpg')
	addDir('ALL', url, 2, artfolder + 'tudo.jpg')

def url_video(url):
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('SuperAnimes', 'A resolver link', 'Por favor aguarde...')
	mensagemprogresso.update(50)

	codigo_fonte = abrir_url(url).result
	soup = BeautifulSoup(codigo_fonte)
	video = str(soup.find('video', id = 'example_video_1'))
	vurl = re.compile(r'<source src="(.*?)" type=.+?>').findall(video)
	vurl = str(vurl).replace("['","").replace("']","")
	player(vurl)

def player(url):
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('SuperAnimes', 'A resolver link', 'Por favor aguarde...')
	mensagemprogresso.update(100)

	listitem = xbmcgui.ListItem()  # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
	listitem.setPath(url)
	listitem.setProperty('mimetype', 'video/mp4')
	listitem.setProperty('IsPlayable', 'true')
	# try:
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(url)

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


def addDir(name, url, mode, iconimage, pasta=True, total=1):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)
	return ok


############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params) - 1] == '/'):
			params = params[0:len(params) - 2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]

	return param


params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass

try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "Iconimage: " + str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode == None or url == None or len(url) < 1:
	print ""
	CATEGORIES()

elif mode == 1:
	print ""
	letras(url)

elif mode == 2:
	print ""
	montar_url(url, name)

elif mode == 3:
	print ""
	listar_animes(url)

elif mode == 4:
	print ""
	listar_animes2(url)

elif mode == 5:
	print ""
	url_video(url)

elif mode == 6:
	print ""
	listar_lancamentos(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))

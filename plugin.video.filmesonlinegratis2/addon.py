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
# gutoakashi1   07/06/2015


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, HTMLParser, xmltosrt
import urlresolver
import jsunpack
import html5lib
from bs4 import BeautifulSoup

try:
    import json
except:
    import simplejson as json

h = HTMLParser.HTMLParser()

versao = '0.1.3'
addon_id = 'plugin.video.filmesonlinegratis2'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'


############################################### MENUS############################################


def CATEGORIES():
	dialog = xbmcgui.Dialog()
	#dialog.ok("Atualizado", "Addon atualizado por gutoakashi1. email: akx.kodi@bol.com.br")
	#dialog = xbmcgui.Dialog()
	#dialog.ok("Doações",
	#		  "Faça sua doação para manter o addon sempre atualizado. Mande um email para akx.kodi@bol.com.br para mais informações")
	addDir('CATEGORIAS', '-', 1, artfolder + 'categorias.png')
	addDir('LANCAMENTOS', 'http://www.filmesonlinegratis.net/filmes-lancamentos', 2, artfolder + 'categorias.png')
	addDir('SERIADOS', 'http://www.filmesonlinegratis.net/series', 5, artfolder + 'destaques.png')
	addDir('NOVELAS', 'http://www.filmesonlinegratis.net/novelas', 5, artfolder + 'destaques.png')
	addDir('Pesquisar Filmes', '-', 3, artfolder + 'pesquisar.png')
	addDir('Pesquisar Series', '-', 10, artfolder + 'pesquisar.png')


# addLink("",'',artfolder + '-')  # Esta linha cria um espaço em branco


###############################################FUNCOES#####################################
def categorias():
	addDir('ACAO', 'http://www.filmesonlinegratis.net/acao', 2, artfolder + 'acao.jpg')
	addDir('ANIMACAO', 'http://www.filmesonlinegratis.net/animacao', 2, artfolder + 'animacao.jpg')
	addDir('AVENTURA', 'http://www.filmesonlinegratis.net/aventura', 2, artfolder + 'AVENTURA.jpg')
	addDir('COMEDIA', 'http://www.filmesonlinegratis.net/comedia', 2, artfolder + 'COMEDIA.jpg')
	addDir('COMEDIA ROMANTICA', 'http://www.filmesonlinegratis.net/comedia-romantica', 2, artfolder + 'comediaro.jpg')
	addDir('CRIME', 'http://www.filmesonlinegratis.net/crime', 2, artfolder + 'CRIME.jpg')
	addDir('DOCUMENTARIOS', 'http://www.filmesonlinegratis.net/documentario', 2, artfolder + 'doc.jpg')
	addDir('DRAMA', 'http://www.filmesonlinegratis.net/drama', 2, artfolder + 'DRAMA.jpg')
	addDir('FAROESTE', 'http://www.filmesonlinegratis.net/faroeste', 2, artfolder + 'FAROESTE.jpg')
	addDir('FICCAO CIENTIFICA', 'http://www.filmesonlinegratis.net/ficcao-cientifica', 2, artfolder + 'ficcao.jpg')
	addDir('GUERRA', 'http://www.filmesonlinegratis.net/guerra', 2, artfolder + 'GUERRA.jpg')
	addDir('MUSICAL', 'http://www.filmesonlinegratis.net/musical', 2, artfolder + 'MUSICAL.jpg')
	addDir('POLICIAL', 'http://www.filmesonlinegratis.net/policial', 2, artfolder + 'POLICIAL.jpg')
	addDir('ROMANCE', 'http://www.filmesonlinegratis.net/romance', 2, artfolder + 'ROMANCE.jpg')
	addDir('SUSPENSE', 'http://www.filmesonlinegratis.net/suspense', 2, artfolder + 'SUSPENSE.jpg')
	addDir('TERROR', 'http://www.filmesonlinegratis.net/terror', 2, artfolder + 'TERROR.jpg')
	addDir('THRILLER', 'http://www.filmesonlinegratis.net/thriller', 2, artfolder + 'THRILLER.jpg')


def listar_videos(url):
	codigo_fonte = abrir_url(url).result

	soup = BeautifulSoup(codigo_fonte)
	miniaturas = BeautifulSoup(soup.find("div", {"class": "miniaturas"}).prettify())
	article = str(miniaturas.findAll("article"))
	match = re.compile(r'<a href="(.+?)" title="(.+?)">').findall(article)
	img = re.compile(r'<img alt=".+?" src="(.+?)" title=".+?"/>').findall(article)

	a = []  # url titulo img
	for x in range(0, len(match)):
		temp = [match[x][0], match[x][1], img[x]];
		a.append(temp);

	total = len(a)
	for url2, titulo, img in a:
		titulo = titulo.replace('&#8211;', "-").replace('&#8217;', "'")  # Linha para corrigir caracteres especiais
		img = img.replace('http://static.filmesonlinegratis.net/thumb.php?src=', '')  # Linha para corrigir a foto
		addDir(titulo, url2, 4, img, False, total)  # Linha que eu adicionei
	# addDirPlayer(titulo,url2,4,img,total)  #ver comentarios que fiz na funçao addDirPlayer

	page = re.compile(r'<a class="page larger" href="(.+?)">.+?</a>').findall(codigo_fonte)
	for prox_pagina in page:
		addDir('Página Seguinte >>', prox_pagina, 2, artfolder + 'proxpagina.png')
		break


def listar_series(url):
	codigo_fonte = abrir_url(url).result

	soup = BeautifulSoup(codigo_fonte)
	miniaturas = BeautifulSoup(soup.find("div", {"class": "miniaturas"}).prettify())
	article = str(miniaturas.findAll("article"))
	match = re.compile(r'<a href="(.+?)" title="(.+?)">').findall(article)
	img = re.compile(r'<img alt=".+?" src="(.+?)" title=".+?"/>').findall(article)

	a = []  # url titulo img
	for x in range(0, len(match)):
		temp = [match[x][0], match[x][1], img[x]];
		a.append(temp);

	total = len(a)
	for url2, titulo, img in a:
		titulo = titulo.replace('&#8211;', "-").replace('&#8217;', "'")  # Linha para corrigir caracteres especiais
		img = img.replace('http://static.filmesonlinegratis.net/thumb.php?src=', '')  # Linha para corrigir a foto
		img = img.replace('&amp;w=135&amp;h=185', '')
		addDir(titulo, url2, 6, img, True, total)  # Linha que eu adicionei

	page = re.compile(r'<a class="page larger" href="(.+?)">.+?</a>').findall(codigo_fonte)
	for prox_pagina in page:
		addDir('Página Seguinte >>', prox_pagina, 5, artfolder + 'proxpagina.png')
		break


def listar_temporadas(url):
	codigo_fonte = abrir_url(url).result
	soup = BeautifulSoup(codigo_fonte, "html5lib")
	conteudo = BeautifulSoup(soup.find("ul", {"class": "itens"}).prettify())
	temporadas = conteudo("li")
	total = len(temporadas)

	img = soup.find("div", {"class": "barleft"})
	img = re.findall(r'<img alt=".*?" src="(.*?)" title=".*?"/>', str(img))
	img = str(img).replace("http://static.filmesonlinegratis.net/thumb.php?src=", "").replace("['", "").replace("']",
																												"")
	img = img.replace('&amp;w=135&amp;h=185', '')
	i = 1
	while i <= total:
		titulo = str(i) + " temporada"
		try:
			addDir(titulo, url, 7, img, True, total)
		except:
			pass
		i = i + 1


def listar_series_f2(name, url):
	n = name.replace(' temporada', '')

	soup = BeautifulSoup(abrir_url(url).result, "html5lib")
	try:
		ls(soup, n)
	except:
		ls2(soup, n)


def abrir_series(url):
	serie = Player()
	serie.resolver(url)

def ls(soup, n):

	conteudo = soup.find("li", class_="video"+n+"-code")
	links = conteudo.find_all('td')

	episodios = []

	dublados = links[0]
	dubs = dublados.find_all("a")
	for link in dubs:
		url = link.get('href')
		titulo = link.get_text().encode('utf-8')
		titulo = titulo.replace('Assistir \xe2\x80\x93 ', "") + " - Dublado"
		temp = (url, titulo)
		episodios.append(temp)

	legendados = links[2]
	legs = legendados.find_all("a")
	for link in legs:
		url = link.get('href')
		titulo = link.get_text().encode('utf-8')
		titulo = titulo.replace('Assistir \xe2\x80\x93 ', "") + " - Legendado"
		temp = (url, titulo)
		episodios.append(temp)

	total = len(episodios)
	for url, titulo in episodios:
		addDir(titulo, url, 9, '', False, total)

def ls2(soup, n):

	conteudo = soup.find("li", class_="video" + str(n) + "-code")
	contents = conteudo.find_all_next()

	parada = soup.find("li", class_="video" + str(int(n) + 1) + "-code")
	legenda = soup.find("span", text="Legendado")

	temp = []
	tudo = []
	for content in contents:
		if content == parada:
			break
		elif content == legenda:
			break
		else:
			temp.append(content)

	for content in contents:
		if content == parada:
			break
		else:
			tudo.append(content)

	inteiro = re.findall(r'<a class="bs-episodio" href="(.*?)" rel=.*?>(.*?)</a>', str(tudo))
	dublados = re.findall(r'<a class="bs-episodio" href="(.*?)" rel=.*?>(.*?)</a>', str(temp))
	legendados = inteiro[len(dublados):]

	episodios = []
	for url, titulo in dublados:
		titulo = titulo.replace('Assistir \xe2\x80\x93 ', "") + " - Dublado"
		tempor = (url, titulo)
		episodios.append(tempor)

	for url, titulo in legendados:
		titulo = titulo.replace('Assistir \xe2\x80\x93 ', "") + " - Legendado"
		tempor = (url, titulo)
		episodios.append(tempor)

	total = len(episodios)
	for url, titulo in episodios:
		url = str(url).replace(';','&')
		addDir(titulo, url, 9, '', False, total)


def obtem_neodrive(url):
	codigo_fonte = abrir_url(url).result
	try:
		url_video = re.findall(r'vurl.=."(.*?)";', codigo_fonte)[0]
		return [url_video, "-"]
	except:
		return ["-", "-"]


def obtem_url_videopw(url):
	codigo_fonte = abrir_url(url).result
	try:
		url_video = re.findall(r'var vurl2 = "(.*?)";', codigo_fonte)[0]
		return [url_video, "-"]
	except:
		return ["-", "-"]


def obtem_url_vidzi(url):
	codigo_fonte = abrir_url(url).result
	try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
	except:
		return ["-", "-"]


def obtem_url_vidig(url):
	codigo_fonte = abrir_url(url).result
	try:
		soup = BeautifulSoup(codigo_fonte)
		lista = soup.findAll('script')
		js = str(lista[6]).replace('<script>', "").replace('</script>', "")
		sUnpacked = jsunpack.unpack(js)
		print sUnpacked
		url_video = re.findall(r'file:"(.*?)",provider:', sUnpacked)
		url_video = str(url_video).replace("['", "").replace("']", "")
		return [url_video, "-"]
	except:
		pass


def obtem_url_dropvideo(url):
	codigo_fonte = abrir_url(url).result
	try:
		soup = BeautifulSoup(codigo_fonte)
		lista = soup.findAll('script')
		js = str(lista).replace('<script>', "").replace('</script>', "")
		#print js
		sUnpacked = jsunpack.unpack(js)
		#print sUnpacked
		url_video = re.findall(r'var vurl2="(.*?)";', sUnpacked)
		url_video = str(url_video).replace("['", "").replace("']", "")
		return [url_video, "-"]
	except:
		pass


def play(url):
	h1 = Player()

	def lista_host(url):
		links = []
		hosts = []
		matriz = []
		host = abrir_url(url).result
		return h1.hosts(host, links, hosts, matriz)

	matrix = lista_host(url)

	index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', matrix[0])

	if index == -1:
		return

	url_video = matrix[1][index]
	h1.resolver(url_video)


def play_series(url):

	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('FILMESONLINEGRATIS', 'A resolver link', 'Por favor aguarde...')
	mensagemprogresso.update(33)

	junto = re.findall(r'http://www.filmesonlinegratis.net/eps2/.+?(.*)', url)
	junto = str(junto).replace("['", "").replace("']", "").replace("&amp", "")
	hosts = str(junto).split('&')



	a = []
	for host in hosts:
		url = 'http://www.filmesonlinegratis.net/eps/?' + host
		a.append(url)

	b = []
	for url in a:
		try:
			codigo_fonte = abrir_url(url).result
			soup = BeautifulSoup(codigo_fonte)
			conteudo = soup.find('iframe')
			url_video = conteudo.get('src')
			url_video = 'data-src="' + url_video + '"'
			b.append(str(url_video))
		except:
			pass

	h1 = Player()

	def lista_host(lista):

		links = []
		hosts = []
		matriz = []
		temp = []

		for host in lista:
			temp = h1.hosts(host, links, hosts, matriz)

		return temp

	matrix = lista_host(b)
	index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', matrix[0])
	if index == -1:
		return

	url_video = matrix[1][index]
	h1.resolver(url_video)


class Player(object):
	def hosts(self, codigo_fonte, links, hosts, matriz):
		vidzi = r'data-src="(.*?vidzi.tv/embed-.*?)"'
		dropvideo = r'data-src="(.*?dropvideo.*?/embed.*?)"'
		neodrive = r'data-src="(.*?neodrive.*?/embed.*?)"'
		videopw = r'data-src="(.*?videopw.com/e.*?)"'
		vidig = r'data-src="(.*?vidigvideo.com/embed-.*?)"'

		# print "codigo fonte: " + codigo_fonte
		try:
			links.append(re.findall(vidzi, codigo_fonte)[0])
			hosts.append('Vidzi')
		except:
			pass

		try:
			links.append(re.findall(neodrive, codigo_fonte)[0])
			hosts.append('Neodrive')
		except:
			pass

		try:
			links.append(re.findall(dropvideo, codigo_fonte)[0])
			hosts.append('Dropvideo')
		except:
			pass

		try:
			links.append(re.findall(videopw, codigo_fonte)[0])
			hosts.append('Videopw')
		except:
			pass

		try:
			links.append(re.findall(vidig, codigo_fonte)[0])
			hosts.append('Vidig')
		except:
			pass

		if not hosts:
			return

		return hosts, links

	def resolver(self, url_video):

		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('FILMESONLINEGRATIS', 'A resolver link', 'Por favor aguarde...')
		mensagemprogresso.update(66)
		print 'Player url: %s' % url_video
		if 'neodrive' in url_video:
			matriz = obtem_neodrive(url_video)
		elif 'dropvideo.com/embed' in url_video:
			matriz = obtem_url_dropvideo(url_video)
		elif 'vidzi' in url_video:
			matriz = obtem_url_vidzi(url_video)
		elif 'vidigvideo' in url_video:
			matriz = obtem_url_vidig(url_video)
		elif 'videopw' in url_video:
			matriz = obtem_url_videopw(url_video)
		else:
			print "Falha: " + str(url_video)
		print matriz
		url = matriz[0]
		print url
		if url == '-': return
		legendas = matriz[1]
		print "Url do gdrive: " + str(url_video)
		print "Legendas: " + str(legendas)

		mensagemprogresso.update(100)
		mensagemprogresso.close()

		listitem = xbmcgui.ListItem()  # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
		listitem.setPath(url)
		listitem.setProperty('mimetype', 'video/mp4')
		listitem.setProperty('IsPlayable', 'true')
		# try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url)
		if legendas != '-':
			if 'timedtext' in legendas:
				# legenda = xmltosrt.convert(legendas)
				# try:
				import os.path

				sfile = os.path.join(xbmc.translatePath("special://temp"), 'sub.srt')
				sfile_xml = os.path.join(xbmc.translatePath("special://temp"), 'sub.xml')  # timedtext
				sub_file_xml = open(sfile_xml, 'w')
				sub_file_xml.write(urllib2.urlopen(legendas).read())
				sub_file_xml.close()
				print "Sfile.srt : " + sfile_xml
				xmltosrt.main(sfile_xml)
				xbmcPlayer.setSubtitles(sfile)
			# except:
			#	pass
			else:
				xbmcPlayer.setSubtitles(legendas)


def pesquisa():
	keyb = xbmc.Keyboard('', 'faca a procura')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa = urllib.quote(search)
		url = 'http://www.filmesonlinegratis.net/?s=%s&s-btn=buscar' % str(parametro_pesquisa)
		codigo_fonte = abrir_url(url).result
		soup = BeautifulSoup(codigo_fonte)
		miniaturas = soup.find('div', class_='miniaturas')
		miniaturas = BeautifulSoup(miniaturas.prettify())
		article = str(miniaturas.findAll("article"))
		match = re.compile(r'<a href="(.+?)" title="(.+?)">').findall(article)
		img = re.compile(r'<img alt=".+?" src="(.+?)" title=".+?"/>').findall(article)

		a = []  # url titulo img
		for x in range(0, len(match)):
			temp = [match[x][0], match[x][1], img[x]];
			a.append(temp);

		return a


def pesquisa_filmes():
	a = pesquisa()
	total = len(a)
	for url2, titulo, img in a:
		img = img.replace('//static.filmesonlinegratis.net/thumb.php?src=', '')
		img = img.replace('&amp;w=135&amp;h=185', '')
		addDir(titulo, url2, 4, img, False, total)


def pesquisa_series():
	a = pesquisa()
	total = len(a)
	for url2, titulo, img in a:
		img = img.replace('//static.filmesonlinegratis.net/thumb.php?src=', '')
		img = img.replace('&amp;w=135&amp;h=185', '')
		addDir(titulo, url2, 6, img, True, total)


	###################################################################################


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


def addLink(name, url, iconimage):
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
	return ok


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
	categorias()

elif mode == 2:
	print ""
	listar_videos(url)

elif mode == 3:
	print ""
	pesquisa_filmes()

elif mode == 4:
	print ""
	play(url)

elif mode == 5:
	print ""
	listar_series(url)

elif mode == 6:
	print ""
	listar_temporadas(url)

elif mode == 7:
    print ""
    listar_series_f2(name, url)

elif mode == 8:
    print ""
    abrir_series(url)

elif mode == 9:
    print ""
    play_series(url)

elif mode == 10:
	print ""
	pesquisa_series()

xbmcplugin.endOfDirectory(int(sys.argv[1]))

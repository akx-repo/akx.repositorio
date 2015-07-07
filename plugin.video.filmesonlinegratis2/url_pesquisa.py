__author__ = 'gutoakashi1'

import urllib, urllib2, re
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


url = 'http://www.filmesonlinegratis.net/assistir-orphan-black-todas-as-temporadas-dublado-legendado-online.html'

n = "1"
soup = BeautifulSoup(abrir_url(url).result)

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
    print url
    print titulo

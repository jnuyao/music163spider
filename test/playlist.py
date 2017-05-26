# encoding=utf8
import requests
from bs4 import BeautifulSoup
_session = requests.session()

BASE_URL = 'http://music.163.com/'

for i in range(1, 2):
    url = 'http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset=' + str(i * 35)
    url.decode('utf-8')
    soup = BeautifulSoup(_session.get(url).content, 'lxml')
    aList = soup.findAll('a', attrs={'class': 'tit f-thide s-fc0'})
    for a in aList:
        uri = a['href']
        playListUrl = BASE_URL + uri[1:]
        print playListUrl
        soup = BeautifulSoup(_session.get(playListUrl).content, 'lxml')
        ul = soup.find('ul', attrs={'class': 'f-hide'})
        for li in ul.findAll('li'):
            print li
            songId = (li.find('a'))['href'].split('=')[1]
            print '爬取歌曲ID成功 -> ' + songId

# encoding=utf8
import requests
from bs4 import BeautifulSoup
from config.config import spider_page
import json
from utils import encrypt
from database.yunyinyue import Song, Comment, Commenter
from database.yunyinyue import db

_session = requests.session()
BASE_URL = 'http://music.163.com/'


class SongIdSpider:
    def __init__(self):
        pass

    def song_id_crawl(self):
        # 从第三方出爬取到song_id并保存
        for page in range(spider_page):
            url = 'http://grri94kmi4.app.tianmaying.com/songs?page=' + str(page)
            url.decode('utf-8')
            soup = BeautifulSoup(_session.get(url).content, 'lxml')
            a_list = soup.findAll('a', attrs={'target': '_blank'})
            try:
                for a in a_list:
                    song_id = a['href'].split('=')[1]
                    song = Song.query.filter_by(song_id=int(song_id)).first()
                    if song is None:
                        song = Song(song_id)
                        db.session.add(song)
                try:
                    db.session.commit()
                except Exception, e:
                    db.session.rollback()
                    print e
            except Exception, e:
                print e
        return True

    def get_song_id_list_from_db(self):
        songs = db.session.query(Song).filter(Song.comment_count < 1).all()
        # songs = Song.query.all()
        return songs

    # 从官网的 发现-> 歌单 页面爬取网云音乐的所有歌曲ID
    def get_song_id_list(self):  # 要爬的页数，目前一共42页,爬完42页需要很久很久，可以根据需求选择性设置页数
        songIdList = []
        for i in range(1, spider_page + 1):
            url = 'http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset=' + str(i * 35)
            url.decode('utf-8')
            soup = BeautifulSoup(_session.get(url).content)
            aList = soup.findAll('a', attrs={'class': 'tit f-thide s-fc0'})
            for a in aList:
                uri = a['href']
                playListUrl = BASE_URL + uri[1:]
                soup = BeautifulSoup(_session.get(playListUrl).content)
                ul = soup.find('ul', attrs={'class': 'f-hide'})
                for li in ul.findAll('li'):
                    songId = (li.find('a'))['href'].split('=')[1]
                    print '爬取歌曲ID成功 -> ' + songId
                    songIdList.append(songId)
        # 歌单里难免有重复的歌曲，去一下重复的歌曲ID
        songIdList = list(set(songIdList))
        return songIdList


class SongSpider:
    def __init__(self):
        pass

    def get_song_info(self, song_id):
        url = BASE_URL + 'song?id=' + str(song_id)
        url.decode('utf-8')
        soup = BeautifulSoup(_session.get(url).content, 'lxml')
        str_arr = soup.title.string.split(' - ')
        try:
            singer = str_arr[1]
            name = str_arr[0].encode('utf-8')
            # 去除歌曲名称后面（）内的字，如果不想去除可以注掉下面三行代码
            index = name.find('（')
            if index > 0:
                name = name[0:index]
            result = db.session.query(Song).filter(Song.song_id == song_id)
            for c in result:
                c.name = name
                c.url = url
                c.singer = singer
            # db.session.query(Song).filter(Song.song_id == song_id).update(
            #     {'name': name, 'singer': singer, 'url': url})
            db.session.commit()
        except Exception, e:
            print e
            print soup.title


class SongCommentSpider:
    def __init__(self):
        pass

    def get_song_comment_count(self, song_id):
        # 歌曲评论链接。包含评论与热门评论
        url = BASE_URL + 'weapi/v1/resource/comments/R_SO_4_' + str(song_id) + '/?csrf_token='
        headers = {'Cookie': 'appver=1.5.0.75771;', 'Referer': 'http://music.163.com/'}
        text = {'username': '', 'password': '', 'rememberLogin': 'true'}
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'
        pubKey = '010001'
        text = json.dumps(text)
        secKey = encrypt.createSecretKey(16)
        encText = encrypt.aesEncrypt(encrypt.aesEncrypt(text, nonce), secKey)
        encSecKey = encrypt.rsaEncrypt(secKey, pubKey, modulus)
        data = {'params': encText, 'encSecKey': encSecKey}
        req = requests.post(url, headers=headers, data=data)
        comment_count = req.json()['total']
        result = db.session.query(Song).filter(Song.song_id == song_id)
        for c in result:
            c.comment_count = comment_count

        # 处理comment跟commenter]
        comments_list = req.json()['comments']
        for i in comments_list:
            comment = Comment.query.filter_by(comment_id=int(i['commentId'])).first()
            if comment is None:
                comment = Comment(i['commentId'], song_id, i['user']['userId'], i['content'], i['likedCount'])
                db.session.add(comment)
            commenter = Commenter.query.filter_by(commenter_id=int(i['user']['userId'])).first()
            if commenter is None:
                commenter = Commenter(i['user']['userId'], i['user']['nickname'], i['user']['avatarUrl'])
                db.session.add(commenter)
            try:
                db.session.commit()
            except Exception, e:
                db.session.rollback()
                print e
        hot_comments_list = req.json()['hotComments']
        for i in hot_comments_list:
            comment = Comment.query.filter_by(comment_id=int(i['commentId'])).first()
            if comment is None:
                comment = Comment(i['commentId'], song_id, i['user']['userId'], i['content'], i['likedCount'])
                db.session.add(comment)
            commenter = Commenter.query.filter_by(commenter_id=int(i['user']['userId'])).first()
            if commenter is None:
                commenter = Commenter(i['user']['userId'], i['user']['nickname'], i['user']['avatarUrl'])
                db.session.add(commenter)
            try:
                db.session.commit()
            except Exception, e:
                db.session.rollback()
                print e
        return comment_count

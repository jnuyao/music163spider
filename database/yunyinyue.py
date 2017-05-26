# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
from config.config import DB_URL
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app, session_options={"autoflush": False})


class Song(db.Model):
    """docstring for User"""
    __tablename__ = 'song'
    song_id = db.Column(db.Integer, primary_key=True)
    singer = db.Column(db.String(200))
    name = db.Column(db.String(200))
    url = db.Column(db.String(200))
    comment_count = db.Column(db.Integer)

    def __init__(self, song_id, singer=None, name=None, url=None, comment_count=None):
        # 歌曲id，歌手，歌曲名字，链接，评论总数
        self.song_id = song_id
        self.singer = singer
        self.name = name
        self.url = url
        self.comment_count = comment_count

    def __repr__(self):
        return '<song {}>'.format(self.song_id)


class PlayList(db.Model):
    __tablename__ = 'playlist'
    play_list_id = db.Column(db.Integer, primary_key=True)
    song_id_list = db.Column(db.String(400))

    def __init__(self, play_list_id, song_id_list):
        self.play_list_id = play_list_id
        self.song_id_list = song_id_list

    def __repr__(self):
        return '<song {}>'.format(self.song_id)


class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer)
    commenter_id = db.Column(db.Integer)
    comment_content = db.Column(db.String(400))
    comment_content_like_count = db.Column(db.Integer)

    def __init__(self, comment_id, song_id, commenter_id, comment_content, comment_content_like_count):
        self.comment_id = comment_id
        self.song_id = song_id
        self.commenter_id = commenter_id
        self.comment_content = comment_content
        self.comment_content_like_count = comment_content_like_count

    def __repr__(self):
        return '<song {}>'.format(self.song_id)


class Commenter(db.Model):
    __tablename__ = 'commenter'
    # id = db.Column(db.Integer, primary_key=True)
    commenter_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100))
    avatarUrl = db.Column(db.String(100))

    def __init__(self, commenter_id, nickname, avatarUrl):
        self.commenter_id = commenter_id
        self.nickname = nickname
        self.avatarUrl = avatarUrl

    def __repr__(self):
        return '<song {}>'.format(self.song_id)


if __name__ == '__main__':
    # song = Song(111, '周杰伦', '晴天', 'http://music.163.com', 10)
    # db.session.add(song)
    # db.session.commit()
    # db.session.query(Song).filter(Song.song_id == 60102).update({'name': '天使的翅膀', 'singer': '安琥','url':'http://music.163.com/song?id=60102'})
    # db.session.commit()
    # db.create_all()
    # song = Song(111, '周杰伦', '晴天', 'http://music.163.com', 10)
    # playlist = PlayList(111, 'def@129.com, 1wiwiwieo')
    # comment = Comment(111, 111, '喜欢晴天这首歌', 10)
    # commenter = Commenter(111, 'zhengyaohong', 'http://baidu.com')
    # db.session.add(song)
    # db.session.add(playlist)
    # db.session.add(comment)
    # db.session.add(commenter)
    # db.session.commit()
    songs = Song.query.all()
    for i in songs[0:1]:
        print i.song_id
        db.session.query(Song).filter(Song.song_id == i.song_id).update({'name': 'aaaaa', 'singer': 'aaaaa', 'url': 'aaaaa'})
        db.session.commit()


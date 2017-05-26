# encoding=utf8
from prettytable import PrettyTable
from sqlalchemy import func, text
from database.yunyinyue import Song, Comment
from database.yunyinyue import db


def get_most_comment_count_song():
    song_list = db.session.query(Song).order_by(Song.comment_count.desc()).limit(10).all()
    table = PrettyTable([u'排名', u'评论数', u'歌曲名称', u'歌手'])
    for index, song in enumerate(song_list):
        table.add_row([index + 1, song.comment_count, song.name, song.singer])
    print table


def get_dinglei_comment_count_song():
    song_list = Comment.query.filter_by(commenter_id=48353).order_by(Comment.comment_content_like_count.desc()).limit(
        10).all()
    table = PrettyTable([u'排名', u'评论', u'评论点赞数'])
    for index, song in enumerate(song_list):
        table.add_row([index + 1, song.comment_content, song.comment_content_like_count])
    print table


def get_most_comment_count_singer():
    song_list = db.session.query(Song.singer, func.sum(Song.comment_count).label('total')) \
        .group_by(Song.singer) \
        .order_by(text('total desc')) \
        .limit(10).all()
    table = PrettyTable([u'排名', u'评论数', u'歌手'])
    for index, song in enumerate(song_list):
        table.add_row([index + 1, song.total, song.singer])
    print table


if __name__ == '__main__':
    # get_most_comment_count_song()
    # get_most_comment_count_singer()
    get_dinglei_comment_count_song()

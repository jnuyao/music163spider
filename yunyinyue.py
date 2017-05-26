# encoding=utf8
from spider.yunyinyuespider import SongIdSpider
from spider.yunyinyuespider import SongSpider
from spider.yunyinyuespider import SongCommentSpider
from config import config


# 获取符合条件的歌曲列表
def get_song_list():
    print ' ##正在爬取歌曲编号... ##'
    song_id_spider = SongIdSpider()
    song_id_list = song_id_spider.get_song_id_list_from_db()

    print ' ##爬取歌曲编号完成，共计爬取到' + str(len(song_id_list)) + '首##'
    for song in song_id_list:
        try:
            print '正在处理 song_id 为 ' + str(song.song_id)
            song_comment_spider = SongCommentSpider()
            song_comment_count = song_comment_spider.get_song_comment_count(song.song_id)
            print 'song_id 为 ' + str(song.song_id) + '评论量是 ' + str(song_comment_count)
            if song_comment_count > config.COMMENT_COUNT_LET:
                song_spider = SongSpider()
                song_spider.get_song_info(song.song_id)
                # print '成功匹配一首{名称:', song.name, '-', song.singer
        except Exception, e:
            print e


def main():
    get_song_list()

if __name__ == '__main__':
    main()
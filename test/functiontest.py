# encoding=utf8
from spider.yunyinyuespider import SongIdSpider
from spider.yunyinyuespider import SongSpider
from spider.yunyinyuespider import SongCommentSpider

# 爬取song_id
song_id_spider = SongIdSpider()
song_id_list = song_id_spider.song_id_crawl()

song_comment_spider = SongCommentSpider()
song_comment_count = song_comment_spider.get_song_comment_count(60102)

song_spider = SongSpider(60102)
song_spider.get_song_info()

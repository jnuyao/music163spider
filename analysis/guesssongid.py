# encoding=utf8
from spider.yunyinyuespider import SongIdSpider
import pylab as pl

song_id_spider = SongIdSpider()
song_id_list = song_id_spider.get_song_id_list_from_db()
x = range(1, len(song_id_list) + 1)[75:200]
y = [i.song_id for i in song_id_list][75:200]
pl.plot(x, y)
pl.show()

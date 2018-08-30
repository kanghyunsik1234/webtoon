import requests
from bs4 import BeautifulSoup
import random

url = "https://comic.naver.com/webtoon/weekday.nhn"
req = requests.get(url).text
doc = BeautifulSoup(req, 'html.parser')

#comic = doc.select('#content > div.list_area.daily_all > div > div > ul > li > a')[0].text

title_tag = doc.select('div.col_inner > ul > li > a')
img_tag = doc.select('div.thumb > a > img')
#print(img_tag[0])
#print(len(title_tag))
list_comics = []

for i in title_tag:
    list_comics.append(i.text)
print(len(list_comics))

comic_dic ={}

for i in range(0,10):
    comic_dic[i] = {
        "title": title_tag[i].text,
        "photo": img_tag[i].get('src'),
    }



pick_comic = comic_dic[random.randrange(0,10)]
#print(len(pick_comic))

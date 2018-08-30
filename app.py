import os
import json
from flask import Flask, request, jsonify
import random
import requests
app = Flask(__name__)
from bs4 import BeautifulSoup

@app.route('/')
def hello():
    return '챗봇페이지 입니다!!!!'

@app.route('/keyboard')
def keyboard():
    #keyboard 딕셔너리 생성
    keyboard = {
        "type" : "buttons",
        "buttons" : ["Movie", "Webtoon", "Dog", "Lotto"]
    }
    # json으로 변환
    json_keyboard = json.dumps(keyboard)
    return json_keyboard
    
@app.route('/message', methods=['POST'])
def message():
    
    # content라는 key의 value를 msg에 저장
    msg = request.json['content']
    img_bool = False
    if msg == "Movie":
        width = 720
        height = 640
        img_bool = True
        url = "https://movie.naver.com/movie/running/current.nhn"
        req = requests.get(url).text
        soup = BeautifulSoup(req, 'html.parser')
        img_tag = soup.select('div.thumb > a > img')
        
        title_tag = soup.select('dl.lst_dsc > dt > a')
        star_tag = soup.select('dl.lst_dsc > dd.star > dl.info_star > dd > div > a > span.num')
        reserve_tag = soup.select('dl.lst_dsc > dd.star > dl.info_exp > dd > div > span.num')
        url_tag = soup.select('div.thumb > a > img')

        movie_dic = {}
        for i in range(0, 10):
            movie_dic[i] = {
                'title':title_tag[i].text,
                'star':star_tag[i].text,
                'reserve':reserve_tag[i].text,
                'url':url_tag[i].get('src')
            }
        pick_movie = movie_dic[random.randrange(0,10)] 
        return_msg = "추천영화: %s/평점:%s/예매율:%s :)" % (pick_movie['title'], pick_movie['star'], pick_movie['reserve'])
        img_url = pick_movie['url']        
    elif msg == "Lotto":
        # 1~45 리스트
        numbers = list(range(1,46))
        pick = random.sample(numbers, 6)
        return_msg = str(sorted(pick))
    
    elif msg =="Dog":
        width = 720
        height = 640
        img_bool = True
        url = "https://api.thedogapi.com/v1/images/search?mime_types=jpg"
        req = requests.get(url).json()
        return_msg = "오늘의 강아지"
        img_url = req[0]['url']
    
    elif msg =="Webtoon":
        width = 83
        height = 90
        img_bool = True
        url = "https://comic.naver.com/webtoon/weekday.nhn"
        req = requests.get(url).text
        doc = BeautifulSoup(req, 'html.parser')
        

#comic = doc.select('#content > div.list_area.daily_all > div > div > ul > li > a')[0].text

        title_tag = doc.select('div.col_inner > ul > li > a')
        img_tag = doc.select('div.thumb > a > img')
#print(img_tag[0])
#print(len(title_tag))
        #list_comics = []

        #for i in title_tag:
            #list_comics.append(i.text)
#print(list_comics)

        comic_dic ={}

        for i in range(0,235):
            comic_dic[i] = {
                "title": title_tag[i].text,
                "photo": img_tag[i].get('src'),
            }
    


        pick_comic = comic_dic[random.randrange(0,235)]
        return_msg = "추천웹툰: %s :)" % (pick_comic["title"])
        img_url = pick_comic['photo']
        
    else:
        return_msg = "웹툰을 클릭하세요 :("
    
        
    if img_bool == True:   
        json_return = {
            "message":{
                "text": return_msg,
                "photo": {
                    "url":img_url,
                    "width":width,
                    "height":height
                }
            },
            "keyboard": {
                "type" : "buttons",
                "buttons" : ["Movie", "Webtoon", "Dog", "Lotto"]
            }
        }
    else:
        json_return = {
            "message":{
                "text": return_msg
            },
            "keyboard": {
                "type" : "buttons",
                "buttons" : ["Movie", "Webtoon", "Dog", "Lotto"]
            }
        }
    
    return jsonify(json_return)
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

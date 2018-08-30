import os
import json
from flask import Flask, request, jsonify
import random
import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return '챗봇페이지 입니다!!!!'

@app.route('/keyboard')
def keyboard():
    #keyboard 딕셔너리 생성
    keyboard = {
        "type" : "buttons",
        "buttons" : ["ho", "ye", "on"]
    }
    # json으로 변환
    json_keyboard = json.dumps(keyboard)
    return json_keyboard
    
@app.route('/message', methods=['POST'])
def message():
    
    # content라는 key의 value를 msg에 저장
    msg = request.json['content']
    img_bool = False
    if msg == "ho":
        list2 = ["웹툰1", "웹툰2", "웹툰3", "웹툰4"]
        return_msg = random.choice(list2)
    elif msg == "ye":
        # 1~45 리스트
        numbers = list(range(1,46))
        pick = random.sample(numbers, 6)
        return_msg = str(sorted(pick))
    
    elif msg =="on":
        img_bool = True
        url = "https://api.thedogapi.com/v1/images/search?mime_types=jpg"
        req = requests.get(url).json()
        dog_url = req[0]['url']

    else:
        return_msg = "웹툰을 클릭하세요 :("
    
        
    if img_bool == True:   
        json_return = {
            "message":{
                "text": "강아지",
                "photo": {
                    "url":dog_url,
                    "width":720,
                    "height":640
                }
            },
            "keyboard": {
                "type" : "buttons",
                "buttons" : ["ho", "ye", "on"]
            }
        }
    else:
        json_return = {
            "message":{
                "text": return_msg
            },
            "keyboard": {
                "type" : "buttons",
                "buttons" : ["ho", "ye", "on"]
            }
        }
    
    return jsonify(json_return)
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

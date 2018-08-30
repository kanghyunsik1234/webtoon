import os
import json
from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello():
    return '챗봇페이지 입니다!!!!'

@app.route('/keyboard')
def keyboard():
    keyboard = {
        "type" : "buttons",
        "buttons" : ["ho", "ye", "on"]
    }
    json_keyboard = json.dumps(keyboard)
    return json_keyboard
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

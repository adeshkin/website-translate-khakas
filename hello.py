from flask import Flask
import urllib.parse
import sqlite3
from flask import request
import requests

application = Flask(__name__)


sqlite_connection = sqlite3.connect('translate.db')

def getFromBase(typeT, text):
    #sqlite_connection = sqlite3.connect('translate.db')
    cursor = sqlite_connection.cursor()
    sqlite_select_query = "select translate from `" + typeT.replace('-', '') + "` WHERE word='" + text + "'"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchone()
    return record

with open('jsapp.js', 'r', encoding='utf-8') as file:
    jsapp = file.read()

with open('styles.css', 'r', encoding='utf-8') as file:
    styles = file.read()

with open('static/image/back.svg') as file:
    back = file.read()

styles = styles.replace('!back!', urllib.parse.quote(back))

with open('index1.html', 'r', encoding='utf-8') as file:
    body = file.read()

with open('static/image/logo.svg') as file:
    logo = file.read()

body = body.replace('!jsapp!', jsapp).replace('!styles!', styles).replace('!logo!', logo)

@application.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        typeTranslate = request.form.get('type')
        inputSentence = request.form.get('text').replace('ҷ', 'ӌ')
        
        count = len(inputSentence.split())
        if count == 1:
            #inputSentence = inputSentence.replace(' ', '')
            res = inputSentence.replace('ӌ', 'ҷ') #getFromBase(typeTranslate, inputSentence)
        else:
            #url = 'https://195b.ngrok-free.app/predict'
            #answer = requests.get(url, params={'text': inputSentence, 'type': typeTranslate}).json()
            #res = answer['translation'].replace('ӌ', 'ҷ')
            res = inputSentence.replace('ӌ', 'ҷ')
            speech = 'null' #answer['speech']
            if res == 'null':
                res = None
            if speech == 'null':
                speech = None
            #if '<!doctype' in answer.lower():
            #    res = None
    
        return {'main_word': res if res else inputSentence,'speech':speech if speech else 'null'} 
        
    return body


if __name__ == "__main__":
   application.run(host='0.0.0.0', debug=True)
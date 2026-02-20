import urllib.parse
import sqlite3
from inference import translate_sent


sqlite_connection = sqlite3.connect('translate.db')

with open('jsapp.js', 'r', encoding='utf-8') as file:
    jsapp = file.read()

with open('styles.css', 'r', encoding='utf-8') as file:
    styles = file.read()

with open('static/image/back.svg') as file:
    back = file.read()

styles = styles.replace('!back!', urllib.parse.quote(back))

with open('index.html', 'r', encoding='utf-8') as file:
    body = file.read()

with open('static/image/logo.svg') as file:
    logo = file.read()

body = body.replace('!jsapp!', jsapp).replace('!styles!', styles).replace('!logo!', logo)


def getFromBase(typeT, text):
    sqlite_connection = sqlite3.connect('translate.db')
    cursor = sqlite_connection.cursor()
    sqlite_select_query = "select translate from `" + typeT.replace('-', '') + "` WHERE word='" + text + "'"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchone()
    return record


def handler(event, context):
    if 'text' not in event['queryStringParameters'] and 'type' not in event['queryStringParameters']:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'isBase64Encoded': False,
            'body': body
        }
    else:
        typeTranslate = event['queryStringParameters']['type']
        inputSentence = event['queryStringParameters']['text'].lower()
        count = len(inputSentence.split())
        if count == 1:
            inputSentence = inputSentence.replace(' ', '')
            res = getFromBase(typeTranslate, inputSentence)
            if not res:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'text/html'
                    },
                    'isBase64Encoded': False,
                    'body': {"main_word": inputSentence}
                }
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html'
                },
                'isBase64Encoded': False,
                'body': {"main_word": res}
            }
        trans_sent = translate_sent(inputSentence)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'isBase64Encoded': False,
            'body': {"main_word": trans_sent}
        }

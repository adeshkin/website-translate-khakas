from flask import Flask, request
import requests
from prepare_input_text import prepare_input_text
from search_in_word_dict import search_in_word_dict


app = Flask(__name__)


@app.route("/predict")
def predict():
    translation = 'null'
    speech = 'null'
    try:
        text = request.args.get('text')
        direct = request.args.get('type')

        text, num_tokens = prepare_input_text(text)
        if num_tokens == 1:
            return search_in_word_dict(text)
        else:
            if direct == 'kh-ru':
                try:
                    url = 'http://127.0.0.1:13001/predict'
                    translation = requests.get(url, params={'text': text}).text
                except:
                    translation = 'null'
                    print('kh-ru is not available')
                speech = 'null'
            elif direct == 'ru-kh':
                try:
                    url = 'http://127.0.0.1:13002/predict'
                    translation = requests.get(url, params={'text': text}).text
                except:
                    translation = 'null'
                    print('ru-kh is not available')
                # if translation != 'null':
                #     try:
                #         s_url = 'http://127.0.0.1:13003/predict'
                #         speech = requests.get(s_url, params={'text': translation}).text
                #     except:
                #         speech = 'null'
                #         print('text-to-speech is not available')
                speech = 'null'
            else:
                print(f'{direct} is not supported')
    except Exception as error:
        print("An exception occurred:", type(error).__name__, "–", error)

    return {'translation': translation, 'speech': speech}


if __name__ == '__main__':
    app.run(port=13000)
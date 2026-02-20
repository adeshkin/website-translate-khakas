import torch
import os
import io
from flask import Flask, request


template_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir)
torch._C._jit_set_profiling_mode(False)
device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'model.pt'
speaker = 'b_kjh'
sample_rate = 48000
if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/cyr/v4_cyrillic.pt',
                                   local_file)

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)

# warmup
for _ in range(10):
    text1 = 'Республиканың ааллардағы ат спорты марығларының халғанӌы чардығы.'
    audio_path1 = model.save_wav(text=text1,
                                 speaker=speaker,
                                 sample_rate=sample_rate)
from flask import send_file, make_response
from flask import Response
import wave
@app.route("/predict")
def predict():
    try:
        text = request.args.get('text')
        audio_path = model.save_wav(text=text,
                                     speaker=speaker,
                                     sample_rate=sample_rate)
        response = make_response(send_file(audio_path))
        response.headers['Custom-Text'] = 'text'
        # from pydub import AudioSegment
        #
        # sound = AudioSegment.from_wav(audio_path)
        # new_audio_path = 'test.mp3'
        # sound.export(new_audio_path, format="mp3")
        # with open(audio_path, 'rb') as f:
        #     audio = f.read()
        # #os.remove(audio_path)
        # print(len(audio))
        # audio = model.apply_tts(text=text,
        #                         speaker=speaker,
        #                         sample_rate=sample_rate)
        # audio = (audio * 32767).numpy().astype('int16').tolist()
    except:
        audio = 'null'

    #return Response(audio, mimetype='audio/wav')
    return response
    # return audio

# from flask import render_template
# @app.route("/text_to_speech/<text>")
# def text_to_speech(text):
#     audio_path = model.save_wav(text=text,
#                                      speaker=speaker,
#                                      sample_rate=sample_rate)
#
#     return render_template('audio_map.html')
# from flask import render_template
# @app.route("/")
# def home():
#      return render_template('audio_map.html')

if __name__ == '__main__':
    app.run(port=13003)
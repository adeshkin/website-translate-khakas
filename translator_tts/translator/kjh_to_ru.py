from flask import Flask, request
import torch
from translate_utils import (Seq2SeqTransformer, NUM_ENCODER_LAYERS, NUM_DECODER_LAYERS, EMB_SIZE, SRC_LANGUAGE, TGT_LANGUAGE,
                   NHEAD, SRC_VOCAB_SIZE, TGT_VOCAB_SIZE, FFN_HID_DIM, MAXLEN, k_bpe, text_transform, vocab_transform,
                   translate)

app = Flask(__name__)

device = torch.device('cuda:0')
model_path = '/home/adeshkin/my_projects/nmt/translate-khakas/experiments/nmt_more_kjh_wmt19_thr_2_kk/default_transformer_lang_comb_kjh_kk_ru_lang_kjh_ru_ft/checkpoints/best.pt'
transformer = Seq2SeqTransformer(NUM_ENCODER_LAYERS, NUM_DECODER_LAYERS, EMB_SIZE,
                                 NHEAD, TGT_VOCAB_SIZE, SRC_VOCAB_SIZE, FFN_HID_DIM, MAXLEN)
transformer.load_state_dict(torch.load(model_path, map_location='cpu'))
transformer.to(device)

# warmup
for _ in range(10):
    text1 = 'Республиканың ааллардағы ат спорты марығларының халғанӌы чардығы.'
    src_sent1 = k_bpe.process_line(text1)
    prd_sent_1 = translate(transformer, src_sent1, device, TGT_LANGUAGE, SRC_LANGUAGE, text_transform, vocab_transform)


@app.route("/predict")
def predict():
    answer = 'null'
    try:
        text = request.args.get('text')
        src_sent = k_bpe.process_line(text)
        prd_sent_ = translate(transformer, src_sent, device, TGT_LANGUAGE, SRC_LANGUAGE, text_transform, vocab_transform)
        prd_sent = prd_sent_ + ' '
        answer = prd_sent.replace('@@ ', '').strip()
    except Exception as error:
        print("An exception occurred:", type(error).__name__, "–", error)

    return answer


if __name__ == '__main__':
    app.run(port=13001)

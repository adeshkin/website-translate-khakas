import torch
import sys
sys.path.append('/home/adeshkin/my_projects/nmt/translate-khakas')
from inference.custom_bpe import init_bpe
from data.dataset import tensor_transform, sequential_transforms, tokenize_text
from model import Seq2SeqTransformer
from utils import translate

bpe_dir = '/home/adeshkin/my_projects/nmt/translate-khakas/data/learn_bpe/more_kjh_wmt19_thr_2_kk_ru'
voc_dir = '/home/adeshkin/my_projects/nmt/translate-khakas/data/apply_bpe_more_kjh_wmt19_thr_2_kk_ru'
vocabulary_threshold = 50

SRC_LANGUAGE = 'ru'
TGT_LANGUAGE = 'kjh_kk'
EMB_SIZE = 512
NHEAD = 8
FFN_HID_DIM = 512

NUM_ENCODER_LAYERS = 3
NUM_DECODER_LAYERS = 3
MAXLEN = 350

bpe = init_bpe(bpe_dir, 'ru', vocabulary_threshold)
k_bpe = init_bpe(bpe_dir, 'kjh_kk', vocabulary_threshold)
language_pair_comb = (SRC_LANGUAGE, TGT_LANGUAGE)

vocab_transform = dict()
for lang in language_pair_comb:
    vocab_transform[lang] = torch.load(f'{voc_dir}/vocab_{lang}.pth')

token_transform = dict()
for ln in language_pair_comb:
    token_transform[ln] = tokenize_text

text_transform = {}
for ln in language_pair_comb:
    text_transform[ln] = sequential_transforms(token_transform[ln],
                                               vocab_transform[ln],
                                               tensor_transform)

SRC_VOCAB_SIZE = len(vocab_transform[SRC_LANGUAGE])
TGT_VOCAB_SIZE = len(vocab_transform[TGT_LANGUAGE])
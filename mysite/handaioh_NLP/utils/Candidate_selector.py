from gensim.models import KeyedVectors
from mysite.settings import BASE_DIR
from pathlib import Path
import random

data_path = str(Path(BASE_DIR).joinpath('handaioh_NLP/utils/data/word2vec.300d.ja.txt').resolve())
model = KeyedVectors.load_word2vec_format(data_path)


def Candidate_selector(word, topn=3):
    return [word for (word, _) in model.most_similar(word, topn=topn)] if word in model.wv.vocab else None

def digit_candidate(num):
    Int_Frac = num.split('.')
    Int_part = Int_Frac[0] if len(Int_Frac[0]) > 0 else '0'
    Frac_part = str('.' + '.'.join(Int_Frac[1:])) if len(Int_Frac) > 1 else ''
    margin = random.sample([i for i in range(-int(Int_part[0]) + 1, 10 - int(Int_part[0])) if not i == 0], 3)
    return [str(m * (10 ** (len(Int_part) - 1)) + int(Int_part)) + Frac_part for m in margin]

def quiz_generator():
    return None

if __name__ == '__main__':
    quiz_generator()

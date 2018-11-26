from gensim.models import KeyedVectors
from mysite.settings import BASE_DIR
from pathlib import Path
import random, re
import CaboCha

data_path = str(Path(BASE_DIR).joinpath('handaioh_NLP/utils/data/word2vec.300d.ja.txt').resolve())
model = KeyedVectors.load_word2vec_format(data_path)

repl_align = {
    'LOCATION': 'どこ',
    'PERSON': '誰',
    'O': '何',
}

class Chunk:
    def __init__(self):
        self.words = []
        self.dst = -1
        self.srcs = []
        self.target = False

    def __str__(self):
        return ' '.join(['{}({}|{})'.format(word['word'], word['POS'], word['NE']) for word in self.words]) + str(self.dst)

def dep_analysis(deps, target):
    chunk = {}
    for line in deps:
        if line[0] == '*':
            chunk_col = line.split(' ')
            dst = int(re.search(r'(.*?)D', chunk_col[2]).group(1))
            idx = int(chunk_col[1])
            if idx not in chunk: chunk[idx] = Chunk()
            chunk[idx].dst = dst

            if not dst == -1:
                if dst not in chunk: chunk[dst] = Chunk()
                chunk[dst].srcs.append(idx)

        elif line == 'EOS':
            continue

        else:
            col1 = line.split('\t')
            col2 = col1[1].split(',')
            if col1[0] == target: chunk[idx].target = True
            chunk[idx].words.append({'word': col1[0],
                                     'POS': col2[0],
                                     'NE': col1[2].split('-')[-1]})
    return list(list(zip(*sorted(chunk.items(), key=lambda x:x[0])))[1])

def quiz_generator(raw_sentence, target):
    c = CaboCha.Parser('-f1 -n1')
    deps = c.parseToString(raw_sentence).split('\n')
    deps = deps[:-3] if deps[-3][0] == '。' else deps[:-2]
    deps = dep_analysis(deps, target)
    [print(chunk) for chunk in deps]
    if deps[-1].words[-1]['POS'] == '名詞':
        for idx, chunk in enumerate(deps):
            if chunk.target:
                # 最後の文節に係っている文節は単純に変形可能
                if chunk.dst == len(deps)-1:
                    target_phrase = deps.pop(idx)
                    question_phrase = repl_align[[word['NE'] for word in target_phrase.words if word['word'] == target][0]]
                    question_phrase = 'したのは{}でしょう？'.format(question_phrase)
                    quiz = ''.join([word['word'] for chunk in deps for word in chunk.words]) + question_phrase
                    return quiz, True
                else:
                    base_sentence = ''.join([word['word'] for chunk in deps for word in chunk.words])
                    question_phrase = repl_align[[word['NE'] for word in deps[idx].words if word['word'] == target][0]]
                    quiz = base_sentence.replace(target, question_phrase) + 'したでしょう？'
                    return quiz, True
    else: return raw_sentence.replace(target, '[question]'), False

def Candidate_selector(word, topn=3):
    return [word for (word, _) in model.most_similar(word, topn=topn)] if word in model.wv.vocab else None

def digit_candidate(num):
    Int_Frac = num.split('.')
    Int_part = Int_Frac[0] if len(Int_Frac[0]) > 0 else '0'
    Frac_part = str('.' + '.'.join(Int_Frac[1:])) if len(Int_Frac) > 1 else ''
    margin = random.sample([i for i in range(-int(Int_part[0]) + 1, 10 - int(Int_part[0])) if not i == 0], 3)
    return [str(m * (10 ** (len(Int_part) - 1)) + int(Int_part)) + Frac_part for m in margin]


if __name__ == '__main__':
    quiz_generator()

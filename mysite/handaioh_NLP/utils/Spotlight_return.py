import spotlight
import random
from pprint import pprint
from mysite.settings import BASE_DIR
from pathlib import Path
import sys
sys.path.append(str(Path(BASE_DIR).joinpath('handaioh_NLP/utils/').resolve()))
from Candidate_selector import Candidate_selector

spotlight_server = 'http://localhost:2250/rest/annotate'
# spotlight_server = 'http://10.0.16.1:2250/rest/annotate'

def Spotlight_return(sentence):
    annotations = spotlight.annotate(spotlight_server, sentence)
    rand_list = list(range(len(annotations)))
    random.shuffle(rand_list)
    for num in rand_list:
        pick_up = annotations[num]
        if Candidate_selector(pick_up['surfaceForm']) != None:
            break

    data = {
        'dbpedia_entity': pick_up['URI'].split('/')[-1],
        'word'          : pick_up['surfaceForm'],
        'q_sentence'    : sentence.replace(pick_up['surfaceForm'], '[question]'),
        'origin_text'   : sentence
    }
    return data


def Spotlight_vocab(word):
    try:
        spotlight.annotate(spotlight_server, word)
        return True
    except:
        return False

def check_spotlight(tweets_list):
    quiz_cand_list = []
    for i in range(len(tweets_list)):
        text = tweets_list[i]['text']
        title = tweets_list[i]['title']
        try:
            annotations_text = spotlight.annotate(spotlight_server, text)
            annotations_title = spotlight.annotate(spotlight_server, title)

            text_surfaceform = {word['surfaceForm'] for word in annotations_text}
            title_surfaceform = {word['surfaceForm'] for word in annotations_title}
            blank_list_cand = list(text_surfaceform & title_surfaceform)
            blank_list = []
            for j in range(len(blank_list_cand)):
                word = blank_list_cand[j]
                if Candidate_selector(word):
                    blank_list.append(word)
            if len(blank_list) != 0:
                blank_cand = '_'.join(blank_list)
                tweets_list[i].update({'blank_cand':blank_cand})
                quiz_cand_list.append(tweets_list[i])
        except:
            pass
    return quiz_cand_list

if __name__ == '__main__':
    data = Spotlight_return('NASAは8月に打ち上げられた太陽探査機が、太陽に最も接近した人工物として新記録を達成したと発表。')
    word1, word2 = 'NASA', 'NASAAAA'
    pprint(data)
    print(Spotlight_vocab(word1), Spotlight_vocab(word2))

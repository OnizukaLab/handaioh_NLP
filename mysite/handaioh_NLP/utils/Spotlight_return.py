import spotlight
import random
from pprint import pprint
# from Candidate_selector import Candidate_selector

spotlight_server = 'http://localhost:2250/rest/annotate'

def Spotlight_return(sentence):
    annotations = spotlight.annotate(spotlight_server, sentence)
    pick_up = annotations[random.randrange(0, len(annotations))]
    data = {
        'dbpedia_entity': pick_up['URI'].split('/')[-1],
        'word'          : pick_up['surfaceForm'],
        'q_sentence'    : sentence.replace(pick_up['surfaceForm'], '<question>'),
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
        try:
            annotations = spotlight.annotate(spotlight_server, text)
            for j in range(len(annotations)):
                word = annotations[j]['URI'].split('/')[-1]
                # if Candidate_selector(word):
                #     quiz_cand_list.append(tweets_list[i])
                #     break
            quiz_cand_list.append(tweets_list[i])
        except:
            pass
    return quiz_cand_list

if __name__ == '__main__':
    data = Spotlight_return('NASAは8月に打ち上げられた太陽探査機が、太陽に最も接近した人工物として新記録を達成したと発表。')
    word1, word2 = 'NASA', 'NASAAAA'
    pprint(data)
    print(Spotlight_vocab(word1), Spotlight_vocab(word2))

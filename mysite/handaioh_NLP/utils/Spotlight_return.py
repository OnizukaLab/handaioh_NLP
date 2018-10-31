import spotlight
import random
from pprint import pprint

spotlight_server = 'http://localhost:2250/rest/annotate'

def Spotlight_retun(sentence):
    annotations = spotlight.annotate(spotlight_server, sentence)
    pick_up = annotations[random.randrange(0, len(annotations))]
    data = {
        'dbpedia_entity': pick_up['URI'].split('/')[-1],
        'word'          : pick_up['surfaceForm'],
        'q_sentence'    : sentence.replace(pick_up['surfaceForm'], '<question>')
    }
    return data


if __name__ == '__main__':
    data = Spotlight_retun('NASAは8月に打ち上げられた太陽探査機が、太陽に最も接近した人工物として新記録を達成したと発表。')
    pprint(data)

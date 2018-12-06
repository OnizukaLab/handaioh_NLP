from django.http import HttpResponse, JsonResponse
import sys
from rest_framework import viewsets
from .models import Quiz
from .serializer import QuizSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from .utils.Spotlight_return import Spotlight_return
from .utils.Candidate_selector import Candidate_selector, digit_candidate, quiz_generator

sys.path.append('handaioh_NLP/utils/')

class QuizViewSet(APIView):
    def get(self, request):
        queryset = Quiz.objects.all()
        serializer_class = QuizSerializer(queryset, many=True)
        res = self.make_response(serializer_class.data)
        return Response(res, status.HTTP_200_OK)

    def make_response(self, data):
        qid = random.randint(0,len(data)-1)
        target_word = random.choice(data[qid]['blank_cand'].split('_'))
        digit_flg = False

        if target_word.isdigit():
            digit_flg = True
            convert_flg = False
            candidates = digit_candidate(target_word)
            quiz = {'dbpedia_entity': '数字','word': target_word,
                    'q_sentence': data[qid]['text'].replace(target_word, '[question]', 1),'origin_text': data[qid]['text']}
        else:
            quiz = Spotlight_return(data[qid]['text'], target_word)
            quiz['q_sentence'], convert_flg = quiz_generator(quiz['origin_text'], quiz['word'])
            candidates = Candidate_selector(quiz['dbpedia_entity'])
            if candidates is None: candidates = ['___', '___', '___']


        candidates.append(target_word)
        random.shuffle(candidates)
        ans = candidates.index(target_word)

        second_text = data[qid]['second_text']
        title = data[qid]['title']
        favorite_count = data[qid]['favorite_count']
        retweet_count = data[qid]['retweet_count']
        date_inf = data[qid]['date_inf']

        return_data = {
            'quiz'          : quiz['q_sentence'],
            'candidate'     : candidates,
            'title'         : title,
            'second_text'   : second_text,
            'ans_word'      : target_word,
            'ans_id'        : ans,
            'entity_name'   : quiz['dbpedia_entity'],
            'favorite_count': favorite_count,
            'retweet_count' : retweet_count,
            'date_inf'      : date_inf,
            'digit_flg'     : digit_flg,
            'convert_flg'   : convert_flg
        }
        return return_data


def create_question(request):
    return JsonResponse({'hogehoge':'lalalalala'})


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
from .utils.Candidate_selector import Candidate_selector

sys.path.append('handaioh_NLP/utils/')

class QuizViewSet(APIView):
    def get(self, request):
        queryset = Quiz.objects.all()
        serializer_class = QuizSerializer(queryset, many=True)
        res = self.make_response(serializer_class.data)
        return Response(res, status.HTTP_200_OK)

    def make_response(self, data):
        qid = random.randint(0,len(data)-1)

        quiz = Spotlight_return(data[qid]['text'])
        # for testing
        # quiz = {'dbpedia_entity': '組織' , 'word': 'NASA', 'q_sentence': '____は8月に打ち上げられた太陽探査機が、太陽に最も接近した人工物として新記録を達成したと発表。'}
        candidates = Candidate_selector(quiz['word'])
        candidates.append(quiz['word'])
        random.shuffle(candidates)
        ans = candidates.index(quiz['word'])
        if candidates is None: candidates = ['___', '___', '___']
        return {'quiz': quiz['q_sentence'], 'candidate': candidates, 'ans_id': ans, 'entity_name': quiz['dbpedia_entity']}






def create_question(request):
    return JsonResponse({'hogehoge':'lalalalala'})


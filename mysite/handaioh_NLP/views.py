from django.http import HttpResponse
import sys
sys.path.append('handaioh_NLP/utils/')

def creat_question(request):
    return HttpResponse("Hello, world. You're at the polls index.")


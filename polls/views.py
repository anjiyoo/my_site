from django.http import HttpResponse
from .models import Question
from django.template import loader

# 뷰 추가하기
# http://127.0.0.1:8000/polls/1/
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

# http://127.0.0.1:8000/polls/2/
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

# http://127.0.0.1:8000/polls/3/
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

# # # 새로운 인덱스
# # from .models import Questio
# def index(request):
# 	# Question 테이블의 pub_date를 정렬해서 최근 5개 값을 변수에 할당
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # 위에서 가져온 데이터에 있는 각 Question의 question_text 속성을 ,로 구분해서 조인
#     output = ", ".join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

# # index 뷰 업데이트
# from django.shortcuts import render
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))


# 단축키 index 뷰 업데이트와 같은 내용
from django.shortcuts import render
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    # index.html 파일 경로
    return render(request, "polls/index.html", context)


# 객체가 존재하지 않을 때 get() 을 사용하여 Http404 예외를 발생
from django.shortcuts import get_object_or_404, render
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})




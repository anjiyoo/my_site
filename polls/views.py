from django.http import HttpResponse
from .models import Question, Choice
from django.template import loader

# 뷰 추가하기
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

# def vote(request, question_id):
#     # choice 데이터에서 해당하는 값에 votes를 1 더하기
#     c = Choice.objects.get(pk=8)
#     c.votes += 1
#     c.save()
#     return HttpResponse("You're voting on question %s." % question_id)

# 단축키 index 뷰 업데이트와 같은 내용
from django.shortcuts import render
def index(request):
    # 최근 추가한 5개 보임
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    # index.html 파일 경로
    return render(request, "polls/index.html", context)


# 객체가 존재하지 않을 때 get() 을 사용하여 Http404 예외를 발생
from django.shortcuts import get_object_or_404, render
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


# vote의 detail 템플릿을 수정 -> form 요소 포함
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
def vote(request, question_id):

    # # choice 데이터에서 해당하는 값에 votes를 1 더하기
    # c = Choice.objects.get(pk=8)
    # c.votes += 1
    # c.save()

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # F() 함수 연산
        # votes 값을 1만큼 증가시키고 저장
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))




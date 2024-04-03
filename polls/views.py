from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.views import generic
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.db.models import F, Sum

# DeleteView
class QuestionDeleteView(generic.DeleteView):
    model = Question
    template_name = 'polls/question_delete.html'
    success_url = reverse_lazy('polls:index')



# ChoiceUpdateView
# 연습문제1.설문조사 앱에서 선택지 업데이트 기능 구현
class ChoiceUpdateView(generic.UpdateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_update_form.html' 
    success_url = reverse_lazy('polls:index')

# UpdateView
class QuestionUpdateView(generic.edit.UpdateView):
    model = Question
    fields = ['question_text', 'pub_date']
    template_name = 'polls/question_update_form.html' 
    success_url = reverse_lazy('polls:index') 



# ChoiceCreateView
# 연습문제1.설문조사 앱에 새로운 선택지 추가 기능 구현
class ChoiceCreateView(generic.edit.CreateView):
    model = Choice
    fields=['choice_text']
    template_name = 'polls/choice_form.html'
    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('polls:detail', kwargs={'question_id': self.kwargs['pk']})

# CreateView
class QuestionCreateView(generic.edit.CreateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/question_form.html'
    success_url = reverse_lazy('polls:index')



# 뷰 개선하기
from django.utils import timezone

def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]



# IndexView
class IndexView(generic.ListView):
    # 페이지 연결
    # [app_name]/[model_name]_list.html
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    # 화면에 표시될 객체
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
    
    # # 연습문제1. 최근 설문조사 질문 목록
    # def get_queryset(self):
    #     return Question.objects.order_by("-pub_date")[:3]
    
    # # 연습문제2. 가장 많은 투표를 받은 질문
    # # q -> q.choice_set.all() : cs -> sum[c.votes for c in cs]
    # # [sum([c.votes for c in q.choice_set.all()] for in Question.objects.all()]
    # # sorted(qs. key=lambda q : sum([c.votes for c in q.choice_set.all()]), reverse=True)
    # def get_queryset(self):
    #     return Question.objects.annotate(total=Sum('choice__votes')).order_by('-total')

    # # 연습문제3. 아직 투표가 없는 질문 목록
    # def get_queryset(self):
    #     return Question.objects.annotate(total=Sum('choice__votes')).filter(total=0)
    

# DetailView
# # 연습문제1
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = "polls/detail.html"

#     def get_object(self):
#         q_id = self.kwargs['question_id']
#         question = get_object_or_404(Question, pk=q_id)
#         return question
    
# 연습문제2
# polls/question_detail.html 생성
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/question_detail.html"

    def get_object(self):
        q_id = self.kwargs['question_id']
        question = get_object_or_404(Question, pk=q_id)
        return question



# ResultsView
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



# 뷰 개선하기
from django.http import Http404

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_object(self, queryset=None):
        """
        Excludes questions that don't have at least one choice.
        """
        # super().get_object() 대신 get_object_or_404를 사용하여 객체를 가져옵니다.
        Question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        if not Question.choice_set.exists():
            raise Http404("No choices found for this question.")
        return Question



# 단축키 index 뷰 업데이트와 같은 내용
def index(request):
    # 최근 추가한 5개 보임
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    # index.html 파일 경로
    return render(request, "polls/index.html", context)



# 객체가 존재하지 않을 때 get() 을 사용하여 Http404 예외를 발생
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # choice_count = len(question.choice_set.all())
    # content_1 = question.choice_set.all()[0]
    question_list = Question.objects.all()
    context ={
        "question" : question,
        "question_list" : question_list
    }
    # context ={
    #     "question" : question,
    #     "ch_num" : choice_count,
    #     "content_1":content_1
    # }
    return render(request, "polls/detail.html", context)



# vote의 detail 템플릿을 수정 -> form 요소 포함
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



# # 뷰 추가하기
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

# def vote(request, question_id):
#     # choice 데이터에서 해당하는 값에 votes를 1 더하기
#     c = Choice.objects.get(pk=8)
#     c.votes += 1
#     c.save()
#     return HttpResponse("You're voting on question %s." % question_id)
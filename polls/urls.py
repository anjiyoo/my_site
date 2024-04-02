from django.urls import path
from . import views

# namespace
app_name = 'polls'

urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/1/
    path("<int:question_id>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/2/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/3/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # CreateView
    path('question/new/', views.QuestionCreateView.as_view(), name='question_new'),
    path('question/<int:pk>/choice/new/', views.ChoiceCreateView.as_view(), name='choice_new'),
    # UpdateView
    path('question/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('choice/<int:pk>/update/', views.ChoiceUpdateView.as_view(), name='choice_update'),
    # DeleteView
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
]
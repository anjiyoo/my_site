from django.urls import path
from . import views
from .views import display_related_choices

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/1/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/2/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/3/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # ex: /polls/4/hello/
    path("<int:question_id>/hello/", views.hello, name="hello"),
]
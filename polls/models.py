from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

# Question 테이블
class Question(models.Model):
    # 문자 필드
    question_text = models.CharField(max_length=200)
    #날짜 및 시간 필드
    pub_date = models.DateTimeField("date published")

    # 매직 메소드 생성
    def __str__(self):
          return self.question_text
    
    @admin.display(
              boolean=True,
              ordering="pub_date",
              description="Published recently?"
    )
    
    # 생성일이 최근인지 체크하는 메소드
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

# Choice 테이블
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # 문자 필드
    choice_text = models.CharField(max_length=200)
    # 정수 필드
    votes = models.IntegerField(default=0)

    # 매직 메소드 생성
    def __str__(self):
          return self.choice_text

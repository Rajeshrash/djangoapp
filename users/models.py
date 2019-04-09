from datetime import datetime
from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class VoteType(Enum):
    UPVOTE = 1
    DOWNVOTE = 2


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=200, default="")
    dob = models.DateField(blank=True, null=True, default=datetime.now)
    is_admin = models.BooleanField(default=False, blank=True)
    is_staff = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name', 'username']

    def __str__(self):
        return self.email


class Question(models.Model):
    question_text = models.CharField(null=False, max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(blank=True, default=datetime.now)

    @staticmethod
    def save_question(user, question_text):
        question = Question(user=user, question_text=question_text)
        question.save()


class Answer(models.Model):
    answer_text = models.CharField(null=False, max_length=10000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(blank=True, default=datetime.now)

    @property
    def upvote_cnt(self):
        return Vote.objects.filter(answer=self, v_type=VoteType.UPVOTE.value).count()

    @property
    def downvote_cnt(self):
        return Vote.objects.filter(answer=self, v_type=VoteType.DOWNVOTE.value).count()

    @staticmethod
    def save_answer(self, answer_text, user, question_id):
        answer = Answer(
            answer_text=answer_text, user=user, question=Question.objects.get(pk=question_id))
        answer.save()

    def upvoted_by_user(self, user):
        upvote = Vote.objects.filter(
            answer=self, user=user, v_type=VoteType.UPVOTE.value)
        return len(upvote) > 0

    def downvoted_by_user(self, user):
        downvote = Vote.objects.filter(
            answer=self, user=user, v_type=VoteType.DOWNVOTE.value)
        return len(downvote) > 0

    def upvote(self, user):
        with transaction.atomic():
            if not self.upvoted_by_user(user):
                vote = Vote(user=user, answer=self,
                            v_type=VoteType.UPVOTE.value)
                vote.save()

            if self.downvoted_by_user(user):
                vote = Vote.objects.filter(
                    user=user, answer=self, v_type=VoteType.DOWNVOTE.value).first()
                vote.delete()

    def downvote(self, user):
        with transaction.atomic():
            if not self.downvoted_by_user(user):
                vote = Vote(user=user, answer=self,
                            v_type=VoteType.DOWNVOTE.value)
                vote.save()

            if self.upvoted_by_user(user):
                vote = Vote.objects.filter(
                    user=user, answer=self, v_type=VoteType.UPVOTE.value).first()
                vote.delete()


class Comment(models.Model):
    comment_text = models.CharField(null=False, max_length=5000)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    date = models.DateField(blank=True, default=datetime.now)

    @staticmethod
    def save_comment(self, comment_text, user, answer):
        comment = Comment(comment_text=comment_text, answer=answer, user=user)
        comment.save()


class Vote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    v_type = models.IntegerField(null=False)

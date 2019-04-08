from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.db import transaction

class VoteType(Enum):
    UPVOTE = 1
    DOWNVOTE = 2


class CustomUser(AbstractUser):

    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=200, default="")
    dob = models.DateField(blank=True,null=True,default=datetime.now)
    is_admin = models.BooleanField(default=False,blank=True)
    is_staff = models.BooleanField(default=False,blank=True)

    USERNAME_FIELD='email'

    REQUIRED_FIELDS=['name','username']

    def __str__(self):
        return self.email


class Question(models.Model):
    question_text=models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateField(blank= True, default = datetime.now)


class Answer(models.Model):
    answer_text = models.CharField(max_length=10000, min_length=0)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateField(blank= True, default = datetime.now)
    # up_vote_count = models.IntegerField(default=0)
    # down_vote_count = models.IntegerField(default=0)

    @property
    def upvote_cnt(self):
        return Vote.objects.count(answer=self, v_type=VoteType.UPVOTE.value)

    @property
    def downvote_cnt(self):
        return Vote.objects.count(answer=self, v_type=VoteType.UPVOTE.value)
        # return Vote.objects.count(answer=self, v_type=VoteType.DOWNVOTE.value)

    def upvoted_by_user(self, user):
        upvote = Upvote.objects.filter(answer=self, user=user)
        return len(upvote) > 0

    def downvoted_by_user(self, user):
        downvote = Downvote.objects.filter(answer=self, user=user)
        return len(downvote) > 0

    def upvote(self, user):
        with transaction.atomic():
            if not self.upvoted_by_user(user):
                vote = Vote(user=user, answer=self, v_type=VoteType.UPVOTE.value)
                vote.save()

            if self.downvoted_by_user(user):
                vote = Vote.objects.filter(
                    user=user,
                    answer=self,
                    v_type=VoteType.DOWNVOTE.value
                ).first()
                vote.delete()

    def downvote(self, user):
        pass



class Comment(models.Model):
    comment_text=models.CharField(max_length=5000)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    date = models.DateField(blank=True, default = datetime.now)


class Vote(models.Model):
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    v_type = models.IntegerField(null=False)


class Upvote(models.Model):
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)


class Downvote(models.Model):
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    @staticmethod
    def delete_vote(user, answer):
        pass

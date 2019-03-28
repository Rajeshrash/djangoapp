from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class CustomUser(AbstractUser):

    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=200, default="")
    dob = models.DateField(blank=True,null=True,default=datetime.now)
    is_admin = models.BooleanField(default=False,blank=True)
    is_staff = models.BooleanField(default=False,blank=True)

    USERNAME_FIELD='email'

    # super.username.help_text = None
    # super.password1.help_text=None
    # super.password2.help_text=None

    REQUIRED_FIELDS=['name','username']

    def __str__(self):
        return self.email

class Question(models.Model):
    question_text=models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateField(blank= True, default = datetime.now)

class Answer(models.Model):
    answer_text = models.CharField(max_length=10000)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateField(blank= True, default = datetime.now)
    up_vote_count = models.IntegerField(default=0)
    down_vote_count = models.IntegerField(default=0)

class Comment(models.Model):
    comment_text=models.CharField(max_length=5000)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    date = models.DateField(blank= True, default = datetime.now)

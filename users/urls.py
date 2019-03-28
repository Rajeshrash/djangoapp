from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('landing/', views.view_all_questions, name='landing'),
    path('save-question/', views.save_question, name='question_save'),
    path('view-all-answers/<int:question_id>',views.view_all_answers,name='view-all-answers'),
    path('save-answer/<int:question_id>' ,views.save_answer,name='save-answer'),
    path('save-comment/<int:answer_id>',views.save_comment,name='save-comment')
]
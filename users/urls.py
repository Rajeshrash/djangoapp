from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('landing/', views.view_all_questions, name='landing'),
    path('save-question/', views.save_question, name='save-question'),
    path('view-all-answers/<int:question_id>',views.view_all_answers,name='view-all-answers'),
    path('save-answer/<int:question_id>' ,views.save_answer,name='save-answer'),
    path('save-comment/<int:answer_id>',views.save_comment,name='save-comment'),
    path('upvote/<int:answer_id>/<int:user_id>',views.upvote,name='upvote'),
    path('downvote/<int:answer_id>/<int:user_id>',views.downvote,name='downvote'),
    path('edit-answer-page/<int:answer_id>',views.edit_page,name="edit-answer-page"),
    path('edit-answer/<int:answer_id>',views.edit_answer,name="edit-answer"),
    path('delete-answer/<int:answer_id>',views.delete_answer,name="delete-answer"),
    path('view-all-answers-by-user/<int:user_id>',views.view_all_answers_by_user,name="view-all-answers-by-user"),
]
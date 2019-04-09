from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('landing/', views.view_all_questions, name='landing'),
    path('save-question/', views.save_question, name='save-question'),
    path('view-all-answers/<int:question_id>',
         views.view_all_answers, name='view-all-answers'),

    path('save-answer/<int:question_id>',
         views.save_answer, name='save-answer'),
    path('save-comment/<int:answer_id>',
         views.save_comment, name='save-comment'),

    path('upvote/<int:answer_id>', views.upvote, name='upvote'),
    path('downvote/<int:answer_id>', views.downvote, name='downvote'),

    path('edit-answer-page/<int:answer_id>',
         views.edit_page, name="edit-answer-page"),
    path('edit-answer/<int:answer_id>', views.edit_answer, name="edit-answer"),
    path('delete-answer/<int:answer_id>',
         views.delete_answer, name="delete-answer"),
    path('view-all-answers-by-user/<int:user_id>',
         views.view_all_answers_by_user, name="view-all-answers-by-user"),
]

# questions/ # questions list
# questions/<question_id> # question detail + answers
# questions/<question_id>/answers/ # all answers for a specific question
# questions/<question_id>/answers/<answer_id>/upvote/ # upvote a specific answer

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import (HttpResponse, HttpResponseRedirect, render,
                              reverse)
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from .models import Answer, Comment, CustomUser, Question, Vote


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('landing')
    template_name = 'signup.html'


# Add try catch to all the functions.

@login_required
def save_question(request):
    if request.method == 'POST':
        if request.POST['question'] == None or request.POST['question'] == "" or request.POST['question'] == " ":
            context = {
                "questions": Question.objects.all()
            }
            return HttpResponseRedirect(reverse('landing'), context)
        Question.objects.create(request.user, request.POST['question'])
        context = {
            "questions": Question.objects.all()
        }
        return HttpResponseRedirect(reverse('landing'), context)
    else:
        raise Http404


def view_all_questions(request):
    questions = Question.objects.all()
    template = 'landing.html'
    context = {
        "questions": questions
    }
    return render(request, template, context)


@login_required
def save_answer(request, question_id):
    if request.method == 'POST':
        print(request.POST['answer'])
        if request.POST['answer'] == None or request.POST['answer'] == "" or request.POST['answer'] == " ":
            return HttpResponseRedirect(reverse('view-all-answers', kwargs={"question_id": question_id}), get_answers_and_comments(question_id))
        Answer.objects.create(
            answer_text=request.POST['answer'],
            user=request.user,
            question_id=question_id
        )
        return HttpResponseRedirect(reverse('view-all-answers', kwargs={"question_id": question_id}), get_answers_and_comments(question_id))
    else:
        raise Http404


@login_required
def save_comment(request, answer_id):
    if request.method == 'POST':
        answer = Answer.objects.get(id=answer_id)
        if request.POST['comment'] == None or request.POST['comment'] == "" or request.POST['comment'] == " ":
            return HttpResponseRedirect(reverse('view-all-answers', kwargs={"question_id": answer.question.id}), get_answers_and_comments(answer.question_id))
        Comment.objects.create(
            comment_text=request.POST['comment'], answer=answer, user=request.user)
        return HttpResponseRedirect(reverse('view-all-answers', kwargs={"question_id": answer.question.id}), get_answers_and_comments(answer.question_id))
    else:
        raise Http404


@login_required
def view_all_answers(request, question_id):
    template = 'view-all-answers.html'
    return render(request, template, get_answers_and_comments(question_id))

# need to implement this and refactor this solving the n+1 query problem
def get_answers_and_comments(question_id):
    pass
    # answers = Answer.objects.filter(
    #     question=Question.objects.get(id=question_id))
    # ans_comments = []
    # for ans in answers:
    #     comments = Comment.objects.filter(answer=ans)
    #     question_response = {
    #         "answer": ans,
    #         "comments": comments
    #     }
    #     ans_comments.append(question_response)
    # context = {
    #     "question_response": ans_comments,
    #     "question": Question.objects.get(id=question_id)
    # }
    # return context


@login_required
def upvote(request, answer_id):
    template = 'view-all-answers.html'
    answer = Answer.objects.get(pk=answer_id)
    answer.upvote(request.user)
    return render(request, template, get_answers_and_comments(answer.question.id))


@login_required
def downvote(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    template = 'view-all-answers.html'
    answer.downvote(request.user)
    return render(request, template, get_answers_and_comments(answer.question.id))


@login_required
def edit_page(request, answer_id):
    template = "edit-answer.html"
    context = {
        "answer": Answer.objects.get(pk=answer_id).answer_text, "answer_id": answer_id
    }
    return render(request, template, context)


@login_required
def edit_answer(request, answer_id):
    if request.method == 'POST' and answer_id is not None:
        answer = Answer.objects.get(pk=answer_id)
        answer.answer_text = request.POST['answer']
        answer.save()
        template = "view-all-answers-by-user.html"
        context = {
            "answers": get_answers_for_user(answer.user.id)
        }
    return render(request, template, context)


@login_required
def delete_answer(request, answer_id):
    if request.method == 'POST' and answer_id is not None:
        user_id = Answer.objects.get(pk=answer_id).user.id
        Answer.objects.get(pk=answer_id).delete()
        context = {
            "answers": get_answers_for_user(user_id)
        }
        template = "view-all-answers-by-user.html"
        return render(request, template, context)
    else:
        raise Http404


@login_required
def view_all_answers_by_user(request, user_id):
    context = {
        "answers": get_answers_for_user(user_id)
    }
    template = "view-all-answers-by-user.html"
    return render(request, template, context)


def get_answers_for_user(user_id):
    return Answer.objects.filter(user=CustomUser.objects.get(pk=user_id))

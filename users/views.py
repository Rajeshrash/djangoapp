from django.shortcuts import render,HttpResponse,HttpResponseRedirect

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Question,Answer,Comment

from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('view-question')
    template_name = 'signup.html'

@login_required
def save_question(request):
    if request.method == 'POST':
        if request.POST['question'] == None or request.POST['question'] == "" or request.POST['question'] ==" ":
            return HttpResponseRedirect("/users/landing",{
            "questions":Question.objects.all()
        })
        question = Question(question_text=request.POST['question'],user =request.user)
        question.save()
        print("Question saved")
        context = {
            "questions":Question.objects.all()
        }
        return HttpResponseRedirect("/users/landing",context)
    else:
        print ("error ocurred")

def view_all_questions(request):
    questions = Question.objects.all()
    context = {
        "questions":questions
    }
    return render(request,'view-questions.html',context)

@login_required
def save_answer(request,question_id):
    if request.method == 'POST':
        if request.POST['answer'] == None or request.POST['answer'] == "" or request.POST['answer'] == " ":
            return render(request,'view-all-answers.html',get_answers_and_comments(question_id))
        question = Question.objects.get(id=question_id)
        answer = Answer(answer_text = request.POST['answer'],user = request.user, question = question, up_vote_count=0,down_vote_count=0)
        answer.save()
        print("Answer saved")
        return render(request,'view-all-answers.html',get_answers_and_comments(question_id))

@login_required
def save_comment(request,answer_id):
    if request.method == 'POST':
        answer = Answer.objects.get(id=answer_id)
        if request.POST['comment'] == None or request.POST['comment'] == "" or request.POST['comment'] == " ":
            return render(request,'view-all-answers.html',get_answers_and_comments(answer.question_id))
        comment = Comment(comment_text = request.POST['comment'],answer= answer,user= request.user)
        comment.save()
        print("Comment saved")
        return render(request,'view-all-answers.html',get_answers_and_comments(answer.question.id))

def view_all_answers(request,question_id):
    return render(request,'view-all-answers.html',get_answers_and_comments(question_id))

def get_answers_and_comments(question_id):
    answers = Answer.objects.filter(question = Question.objects.get(id=question_id))
    ans_comments =[]
    for ans in answers:
        comments = Comment.objects.filter(answer = ans)
        question_response = {
            "answer":ans,
            "comments":comments
        }
        ans_comments.append(question_response)
    context = {
        "question_response":ans_comments,
        "question":Question.objects.get(id=question_id)
    }
    return context




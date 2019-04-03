from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Question,Answer,Comment,CustomUser,Upvote,Downvote
from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('landing')
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
        return HttpResponseRedirect("/users/landing",{ "questions":Question.objects.all()})
    else:
        print ("error ocurred")


def view_all_questions(request):
    questions = Question.objects.all()
    return render(request,'landing.html',{ "questions":questions })


@login_required
def save_answer(request,question_id):
    if request.method == 'POST':
        print(request.POST['answer'])
        if request.POST['answer'] == None or request.POST['answer'] == "" or request.POST['answer'] == " ":
            return HttpResponseRedirect('/users/view-all-answers.html/'+str(question_id),get_answers_and_comments(question_id))
        question = Question.objects.get(id=question_id)
        answer = Answer(answer_text = request.POST['answer'],user = request.user, question = question, up_vote_count=0,down_vote_count=0)
        answer.save()
        return HttpResponseRedirect('/users/view-all-answers/'+str(question_id),get_answers_and_comments(question_id))


@login_required
def save_comment(request,answer_id):
    if request.method == 'POST':
        answer = Answer.objects.get(id=answer_id)
        if request.POST['comment'] == None or request.POST['comment'] == "" or request.POST['comment'] == " ":
            return HttpResponseRedirect('/users/view-all-answers.html/'+str(answer.question.id),get_answers_and_comments(answer.question_id))
        comment = Comment(comment_text = request.POST['comment'],answer= answer,user= request.user)
        comment.save()
        return HttpResponseRedirect('/users/view-all-answers/'+str(answer.question.id),get_answers_and_comments(answer.question.id))


@login_required
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


@login_required
def upvote(request,answer_id,user_id):
    answer = Answer.objects.get(pk=answer_id)
    user = CustomUser.objects.get(pk=user_id)
    upvote = Upvote.objects.filter(answer = answer, user =user)
    if len(upvote) > 0:
        return render(request,'view-all-answers.html',get_answers_and_comments(answer.question.id))
    else:
        upvote = Upvote(user = user, answer = answer)
        upvote.save()
        downvote = Downvote.objects.filter(answer = answer ,user =user)
        if len(downvote) > 0:
            downvote[0].delete()
            answer.down_vote_count -=1
        answer.up_vote_count +=1
        answer.save()
        return render(request,'view-all-answers.html',get_answers_and_comments(answer.question.id))


@login_required
def downvote(request,answer_id,user_id):
    answer = Answer.objects.get(pk=answer_id)
    user = CustomUser.objects.get(pk=user_id)
    downvote = Downvote.objects.filter(answer = answer, user =user)
    if len(downvote) > 0:
        return render(request,'view-all-answers.html',get_answers_and_comments(answer.question.id))
    else:
        downvote = Downvote(user = user, answer = answer)
        downvote.save()
        upvote = Upvote.objects.filter(answer = answer ,user =user)
        if len(upvote) > 0:
            upvote[0].delete()
            answer.up_vote_count -=1
        answer.down_vote_count +=1
        answer.save()
        return render(request,'view-all-answers.html',get_answers_and_comments(answer.question.id))


@login_required
def edit_page(request,answer_id):
    return render(request,"edit-answer.html",{"answer":Answer.objects.get(pk=answer_id).answer_text,"answer_id":answer_id})


@login_required
def edit_answer(request,answer_id):
    if request.method == 'POST' and answer_id is not None:
        answer = Answer.objects.get(pk=answer_id)
        answer.answer_text = request.POST['answer']
        answer.save()
    return render(request,"view-all-answers-by-user.html",{"answers":get_answers_for_user(answer.user.id)})


@login_required
def delete_answer(request,answer_id):
    if request.method == 'POST' and answer_id is not None:
        user_id = Answer.objects.get(pk=answer_id).user.id
        Answer.objects.get(pk=answer_id).delete()
        return render(request,"view-all-answers-by-user.html",{"answers":get_answers_for_user(user_id)})


@login_required
def view_all_answers_by_user(request,user_id):
    return render(request,"view-all-answers-by-user.html",{"answers":get_answers_for_user(user_id)})
    

def get_answers_for_user(user_id):
    return Answer.objects.filter(user=CustomUser.objects.get(pk=user_id))
        

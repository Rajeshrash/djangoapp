from django.shortcuts import render,HttpResponse,HttpResponseRedirect ,reverse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Question,Answer,Comment,CustomUser,Upvote,Downvote
from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('landing')
    template_name = 'signup.html'


#Add try catch to all the functions.

@login_required
def save_question(request):
    if request.method == 'POST':
        if request.POST['question'] == None or request.POST['question'] == "" or request.POST['question'] ==" ":
            context = { 
                "questions":Question.objects.all()
            }
            return HttpResponseRedirect(reverse('landing'), context)
        question = Question(question_text=request.POST['question'],user =request.user)
        question.save()
        context = { 
            "questions":Question.objects.all()
        }
        return HttpResponseRedirect(reverse('landing'), context)
    else:
        raise Http404


def view_all_questions(request):
    questions = Question.objects.all()
    template = 'landing.html'
    context = { 
        "questions":questions 
    }
    return render(request, template, context)


@login_required
def save_answer(request,question_id):
    if request.method == 'POST':
        print(request.POST['answer'])
        if request.POST['answer'] == None or request.POST['answer'] == "" or request.POST['answer'] == " ":
            return HttpResponseRedirect(reverse('view-all-answers', kwargs={ "question_id":question_id }), get_answers_and_comments(question_id)) 
        question = Question.objects.get(id=question_id)
        answer = Answer(answer_text = request.POST['answer'],user = request.user, question = question, up_vote_count=0,down_vote_count=0)
        answer.save()
        return HttpResponseRedirect(reverse('view-all-answers', kwargs={ "question_id":question_id }), get_answers_and_comments(question_id)) 
    else:
        raise Http404


@login_required
def save_comment(request,answer_id):
    if request.method == 'POST':
        answer = Answer.objects.get(id=answer_id)
        if request.POST['comment'] == None or request.POST['comment'] == "" or request.POST['comment'] == " ":
            return HttpResponseRedirect(reverse('view-all-answers',kwargs={"question_id":answer.question.id}),get_answers_and_comments(answer.question_id))
        comment = Comment(comment_text = request.POST['comment'],answer= answer,user= request.user)
        comment.save()
        return HttpResponseRedirect(reverse('view-all-answers',kwargs={"question_id":answer.question.id}),get_answers_and_comments(answer.question_id))
    else:
        raise Http404


@login_required
def view_all_answers(request,question_id):
    template = 'view-all-answers.html'
    return render(request, template ,get_answers_and_comments(question_id))


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
    template = 'view-all-answers.html'
    answer = Answer.objects.get(pk=answer_id)
    user = CustomUser.objects.get(pk=user_id)
    upvote = Upvote.objects.filter(answer = answer, user =user)
    if len(upvote) > 0:
        return render(request, template, get_answers_and_comments(answer.question.id))
    else:
        upvote = Upvote(user = user, answer = answer)
        upvote.save()
        downvote = Downvote.objects.filter(answer = answer ,user =user)
        if len(downvote) > 0:
            downvote[0].delete()
            answer.down_vote_count -=1
        answer.up_vote_count +=1
        answer.save()
        return render(request, template, get_answers_and_comments(answer.question.id))


@login_required
def downvote(request,answer_id,user_id):
    answer = Answer.objects.get(pk=answer_id)
    user = CustomUser.objects.get(pk=user_id)
    template = 'view-all-answers.html'
    downvote = Downvote.objects.filter(answer = answer, user =user)
    if len(downvote) > 0:
        return render(request, template, get_answers_and_comments(answer.question.id))
    else:
        downvote = Downvote(user = user, answer = answer)
        downvote.save()
        upvote = Upvote.objects.filter(answer = answer ,user =user)
        if len(upvote) > 0:
            upvote[0].delete()
            answer.up_vote_count -=1
        answer.down_vote_count +=1
        answer.save()
        return render(request, template, get_answers_and_comments(answer.question.id))


@login_required
def edit_page(request,answer_id):
    template = "edit-answer.html"
    context = {
        "answer":Answer.objects.get(pk=answer_id).answer_text,"answer_id":answer_id
    }
    return render(request, template, context)


@login_required
def edit_answer(request,answer_id):
    if request.method == 'POST' and answer_id is not None:
        answer = Answer.objects.get(pk=answer_id)
        answer.answer_text = request.POST['answer']
        answer.save()
        template = "view-all-answers-by-user.html"
        context = {
            "answers":get_answers_for_user(answer.user.id)
        }
    return render(request, template, context)


@login_required
def delete_answer(request,answer_id):
    if request.method == 'POST' and answer_id is not None:
        user_id = Answer.objects.get(pk=answer_id).user.id
        Answer.objects.get(pk=answer_id).delete()
        context = {
            "answers":get_answers_for_user(user_id)
        }
        template = "view-all-answers-by-user.html"
        return render(request, template, context)
    else :
        raise Http404


@login_required
def view_all_answers_by_user(request,user_id):
    context = {
        "answers":get_answers_for_user(user_id)
    }
    template = "view-all-answers-by-user.html"
    return render(request, template, context)
    

def get_answers_for_user(user_id):
    return Answer.objects.filter(user=CustomUser.objects.get(pk=user_id))
        

from django.db import IntegrityError
from django.core.exceptions import ValidationError
import pytest

from .models import Question, Answer, Vote, Comment, CustomUser


pytestmark = pytest.mark.django_db

# Fixtures

@pytest.fixture
def customuser():
    custom_user = CustomUser(email="rd@gmail.com",username="rajesh_sharma",password="bcdev123")
    custom_user.save()
    return CustomUser.objects.filter(email="rd@gmail.com").first()

@pytest.fixture
def question(customuser):
    Question.objects.create(user=customuser, question_text="New Question1")
    return Question.objects.filter(question_text="New Question1").first()

@pytest.fixture
def answer(customuser,question):
    Answer.objects.create(answer_text="New Answer1", user=customuser, question=question)
    return Answer.objects.filter(answer_text="New Answer1").first()

@pytest.fixture
def comment(customuser,answer):
    Comment.objects.create(comment_text="New Comment1", user=customuser, answer=answer)
    return Comment.objects.filter(comment_text="New Comment1").first()


# Tests for custom user model

def test_for_create_custom_user_without_email():
    with pytest.raises(IntegrityError):
        CustomUser.objects.create(email=None, username="newname",password="bcdev123")

def test_for_create_custom_user_without_username():
    with pytest.raises(IntegrityError):
        CustomUser.objects.create(email="newmail@gmail.com", username=None,password="bcdev123")

def test_for_create_custom_user_without_password():
    with pytest.raises(IntegrityError):
        CustomUser.objects.create(email="newmail@gmail.com", username="newname",password=None)



# Tests for question model

def test_save_question_with_a_user(customuser, question):
    assert question.question_text == "New Question1"

def test_for_storing_question_without_user():
    with pytest.raises(IntegrityError):
        assert Question.objects.create(user=None, question_text="New Question2")

def test_for_storing_question_with_question_text_as_none(customuser):
    with pytest.raises(IntegrityError):
        Question.objects.create(user=None, question_text=None)

def test_for_storing_question_with_question_text_as_duplicates(customuser):
    with pytest.raises(IntegrityError):
        Question.objects.create(user=customuser,question_text="")
        Question.objects.create(user=customuser,question_text="")

def test_for_storing_question_with_question_text_as_empty_string(customuser): # Need to fix
    q = Question.objects.create(user=customuser,question_text="")
    with pytest.raises(ValidationError):
        q.full_clean()


# Tests for answer model

def test_save_answer_for_a_question(customuser, answer):
    assert answer.answer_text == "New Answer1"

def test_for_upvote_by_an_user(customuser, answer):
    answer.upvote(customuser)
    assert answer.upvoted_by_user(customuser) == True

def test_for_downvote_by_an_user(customuser, answer):
    answer.downvote(customuser)
    assert answer.downvoted_by_user(customuser) == True
    
def test_is_upvoted_by_the_user(customuser,answer):
    assert answer.upvoted_by_user(customuser) == False

def test_is_downvoted_by_the_user(customuser,answer):
    assert answer.downvoted_by_user(customuser) == False

def test_for_storing_answer_without_question(customuser,answer):
    with pytest.raises(IntegrityError):
        Answer.objects.create(answer_text="New Answer2", user=customuser, question=None)

def test_for_storing_answer_without_user(question):
    with pytest.raises(IntegrityError):
        Answer.objects.create(answer_text="New Answer2", user=None, question=question)

def test_for_storing_answer_without_answer_text(customuser,question):
    with pytest.raises(IntegrityError):
        Answer.objects.create(answer_text=None, user=customuser, question=question)    

def test_for_storing_answer_with_answer_text_as_duplicates(customuser,question):
    with pytest.raises((IntegrityError)):
        Answer.objects.create(answer_text="", user=customuser, question=question)
        Answer.objects.create(answer_text="", user=customuser, question=question)

def test_for_downvote_count_for_an_answer(customuser, answer):
    answer.downvote(customuser)
    assert answer.downvote_cnt == 1

def test_for_upvote_count_for_an_answer(customuser, answer):
    answer.upvote(customuser)
    assert answer.upvote_cnt == 1

def test_for_storing_answer_text_as_empty_string(customuser,question):
    a = Answer.objects.create(user=customuser, answer_text="", question=question)
    with pytest.raises(ValidationError):
        a.full_clean()


# Tests for comments model

def test_save_comment_for_an_answer(customuser, comment):
    assert comment.comment_text == "New Comment1"

def test_for_storing_comment_without_answer(customuser):
    with pytest.raises(IntegrityError):
        Comment.objects.create(comment_text="New Comment2", user=customuser, answer=None)

def test_for_storing_comment_without_user(customuser, answer):
    with pytest.raises(IntegrityError):
        Comment.objects.create(comment_text="New Comment2", user=None, answer=answer)

def test_for_storing_comment_without_comment_text(customuser, answer):
    with pytest.raises(IntegrityError):
        Comment.objects.create(comment_text=None, user=customuser, answer=answer)

def test_for_store_comments_with_duplicate_comment_text(customuser,answer):
    with pytest.raises(IntegrityError):
        Comment.objects.create(comment_text=" ", user=customuser, answer=answer)
        Comment.objects.create(comment_text=" ", user=customuser, answer=answer)

def test_for_comments_with_comment_text_as_empty_string(customuser,answer):
    c = Comment.objects.create(user=customuser, comment_text="", answer=answer)
    with pytest.raises(ValidationError):
        c.full_clean()
    



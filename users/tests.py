import pytest

from .models import Question, Answer, Vote, Comment, CustomUser

pytestmark = pytest.mark.django_db

@pytest.fixture
def customuser():
    custom_user = CustomUser(email="rd@gmail.com",username="rajesh_sharma",password="bcdev123")
    custom_user.save()
    return CustomUser.objects.filter(email="rd@gmail.com")[0]

@pytest.fixture
def question(customuser):
    Question.save_question(customuser, "New Question1")
    return Question.objects.filter(question_text="New Question1").first()


@pytest.fixture
def answer(customuser,question):
    Answer.save_answer("New Answer1", customuser, question.id)
    return Answer.objects.filter(answer_text="New Answer1").first()

@pytest.fixture
def comment(customuser,answer):
    comment = Comment.save_comment("New Comment1", customuser, answer)
    return Comment.objects.filter(comment_text="New Comment1").first()

def test_save_answer_for_a_question(customuser, answer):
    assert answer.answer_text == "New Answer1"

def test_save_question_with_a_user(customuser, question):
    assert question.question_text == "New Question1"

def test_save_comment_for_an_answer(customuser, comment):
    assert comment.comment_text == "New Comment1"

def test_upvote_count_for_an_answer(customuser, answer):
    answer.upvote(customuser)
    assert answer.upvoted_by_user(customuser) == True

def test_downvote_count_for_an_answer(customuser, answer):
    answer.downvote(customuser)
    assert answer.downvoted_by_user(customuser) == True
    
def test_is_upvoted_by_the_user(customuser,answer):
    assert answer.upvoted_by_user(customuser) == False

def test_is_downvoted_by_the_user(customuser,answer):
    assert answer.downvoted_by_user(customuser) == False

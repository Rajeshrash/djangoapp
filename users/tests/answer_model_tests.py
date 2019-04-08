def answer_should_have_answer_text_field(answer):
    assert answer.save() should raise ValidationErrorException


answer.answer_text = ''


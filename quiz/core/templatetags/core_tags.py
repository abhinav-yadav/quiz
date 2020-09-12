from django.template import Library
from django.urls import reverse
from django.shortcuts import get_object_or_404

from core.models import Question,Option

register = Library()


@register.simple_tag
def option_color(index, option, key, answer):
    index -= 1
    if option == key[index] or option == answer[index]:
        if key[index] == answer[index] or option == answer[index]:
            return 'green'
        else:
            return 'red'
    else:
        return 'black'

@register.simple_tag
def get_question(id):
    question = get_object_or_404(Question, id=id)
    return question


@register.simple_tag
def question_answer(id):
    option = get_object_or_404(Option, id=id)
    if option.answer:
        return '#1cd21c6b'
    return ''

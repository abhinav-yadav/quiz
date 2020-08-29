from django import forms
from .models import (
    Quiz,
    Question,
    Option,
)


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title','image']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['type','question', 'time']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['answer', 'option',]

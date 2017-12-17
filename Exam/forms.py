from django import forms
from .models import *


class ExamForm(forms.ModelForm):

    class Meta:
        model = Exam
        fields = ('name',)


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('number', 'text', 'points',)


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answers
        fields = ('answer', 'correct', )

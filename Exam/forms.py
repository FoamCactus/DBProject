from django import forms
from .models import *


class ExamForm(forms.ModelForm):

    class Meta:
        model = Exam
        fields = ('name',"points")


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('number', 'text')

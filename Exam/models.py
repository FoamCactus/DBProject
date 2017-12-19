from django.db import models
import datetime
from datetime import datetime

class Exam(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    points = models.IntegerField()
    time_of_creation = models.DateTimeField(auto_now_add=True)


class Answers(models.Model):
    answer = models.TextField(max_length=280)
    correct = models.BooleanField(default=False)


class Question(models.Model):
    examName = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = models.TextField(max_length=280)
    number = models.CharField(max_length=3)
    points = models.FloatField(default=1)
    answers = models.ForeignKey(Answers, on_delete=models.CASCADE, default=-1)


class Student(models.Model):
    identifier = models.TextField(max_length=60)


class Results(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    points = models.FloatField(default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
from django.db import models
import datetime
# Create your models here.
class Exam(models.Model):
    name = models.CharField(max_length=30,primary_key=True)
    points = models.IntegerField()
    time_of_creation = models.DateTimeField(default=datetime.datetime.now())
class Question(models.Model):
    examName = models.ForeignKey(Exam, primary_key=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    nummber = models.TextField(max_length=280)
    points = models.FloatField()
class Answers(models.Model):
    examName = models.ForeignKey(Exam, primary_key=True, on_delete=models.CASCADE)
    questionName = models.ForeignKey(Question,primary_key=True,on_delete=models.CASCADE)
    question = models.TextField(max_length=280)
    correct = models.BooleanField(default=False)

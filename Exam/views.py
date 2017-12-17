from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import *
import logging
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def new_test(request):
    return render(request, 'new_test.html')

def studentSignIn(request):
    data = {}
    if request.method == "POST":
        get_value= request.body
        data = json.loads(request.body);
        #TODO add / update this user to the DB using the below
        userId = data["userId"];
        userName = data["userName"];
        email = data["userEmail"];
        logger.error(userId + " " + userName + " " + email);
        user = authenticate(username=email, password=userId)
        login(request)
    return HttpResponse(json.dumps(data), content_type="application/json")

def postNewExam(request):
    data = {}
    exam = {};
    if request.method == "POST":
        #The full, ready to put in DB exam object
        get_value= request.body
        data=json.loads(request.body);
        examName = data["examName"];
        totalPoints = data["totalPoints"];
        exam["name"] = examName;
        exam["points"] = totalPoints;
        # get question list
        questions = data["questions"];
        exam["questions"] = {};
        questionNumber = 1;
        answerNumber = 1;
        for question in questions:
            currentQuestion = "question_" 
            currentQuestion += str(questionNumber);
            questionNumber += 1;
            exam["questions"][currentQuestion] = {};
            questionTitle = questions[question]["title"];
            questionPoints = questions[question]["points"];
            exam["questions"][currentQuestion]["title"] = questionTitle;
            exam["questions"][currentQuestion]["points"] = questionPoints;
            exam["questions"][currentQuestion]["answers"] = {};
            answerList = questions[question]["answers"];
            for answer in answerList:
                currentAnswer = "answer_"
                currentAnswer += str(answerNumber);
                answerNumber += 1;
                exam["questions"][currentQuestion]["answers"][currentAnswer] = {};
                answerText = answerList[answer]["answerText"];
                answerCorrect = answerList[answer]["correct"];
                exam["questions"][currentQuestion]["answers"][currentAnswer]["answerText"] = answerText;
                exam["questions"][currentQuestion]["answers"][currentAnswer]["correct"] = answerCorrect;
    logger.error(exam);
    return HttpResponse(json.dumps(data), content_type="application/json")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def success(request):
    return render(request, 'success.html')

def makeexam(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.points = 10
            exam.save()
            request.session['Exam'] = exam.name
            return redirect('/makequestion')
    else:
        form = ExamForm()
        return render(request,'makeExam.html', {'form':  form})


def makequestion(request):
    if request.method == 'POST':
        form = QuestionForm()
        if form.is_valid():
            question = form.save(commit=False)
            question.examName = request.session['Exam']
            request.session['QNumber'] = question.number
            question.save()
            return redirect('success')
    else:
        form = QuestionForm()
        return render(request, 'makequestions.html', {'form': form})

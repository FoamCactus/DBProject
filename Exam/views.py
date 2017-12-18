from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.models import Group
import logging
logger = logging.getLogger(__name__)

# Create your views here.


@login_required(login_url='/login')
def index(request):
    exams = Exam.objects.all();
    return render(request, 'index.html', { 'exams' : exams })


@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/login/")


def login(request):
    return render(request, 'login.html')


@login_required(login_url='/login')
def new_test(request):
    return render(request, 'new_test.html')


def studentSignIn(request):
    if request.method == "POST":
        data = json.loads(request.body);
        userId = data["userId"];
        userName = data["userName"];
        email = data["userEmail"];
        user, created = User.objects.get_or_create(username=email, email=email);
        if created:
            user.set_password(userId);
            user.first_name = userName.split()[0];
            user.last_name = userName.split()[1];
            user.save();
            # Add user to Studen Group
            studentGroup = Group.objects.get(name="Students");
            studentGroup.user_set.add(user);
        user = authenticate(username=email, password=userId)
        auth_login(request, user)
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required(login_url='/login')
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
        
        # Create exam object + save in DB
        postExam = Exam(name = examName, points = totalPoints);
        postExam.save();
        
        questionNumber = 1;
        answerNumber = 1;
        for question in questions:
            currentQuestion = "question_" 
            currentQuestion += str(questionNumber);
            exam["questions"][currentQuestion] = {};
            questionTitle = questions[question]["title"];
            questionPoints = questions[question]["points"];
            
            exam["questions"][currentQuestion]["title"] = questionTitle;
            exam["questions"][currentQuestion]["points"] = questionPoints;
            exam["questions"][currentQuestion]["answers"] = {};
            answerList = questions[question]["answers"];
            questionNumber += 1;
            for answer in answerList:
                currentAnswer = "answer_"
                currentAnswer += str(answerNumber);
                exam["questions"][currentQuestion]["answers"][currentAnswer] = {};
                answerText = answerList[answer]["answerText"];
                answerCorrect = answerList[answer]["correct"];
                exam["questions"][currentQuestion]["answers"][currentAnswer]["answerText"] = answerText;
                exam["questions"][currentQuestion]["answers"][currentAnswer]["correct"] = answerCorrect;
                
                #Create answer object + post to DB
                postAnswer = Answers(answer = answerText, correct = answerCorrect);
                postAnswer.save();
                       
            #Create question object + save in DB
                postQuestion = Question(text=questionTitle, number = questionNumber, points=questionPoints, examName = Exam.objects.get(name = examName), answers = postAnswer);
                postQuestion.save();

                answerNumber += 1;
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
            teacherGroup = Group.objects.get(name="Teachers");
            teacherGroup.user_set.add(user);            
            if user is not None:
                login(request)
                return redirect('success')
            else:
                return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='/login')
def success(request):
    return render(request, 'success.html')


@login_required(login_url='/login')
def profile(request):
    return render(request, 'profile.html')


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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
    
@login_required(login_url="/login")
def take_test(request, testName):
    exam = Exam.objects.get(name = testName);
    questions = Question.objects.filter(examName = testName);
    questionGroup = {};
    answer = 0;
    for question in questions:
        answer += 1;
        try:
            questionGroup[question.text]["answerGroup"][answer]=question.answers;
            questionGroup[question.text]["question"]= question;
        except:
            questionGroup[question.text] = {};
            questionGroup[question.text]["question"]= question;
            questionGroup[question.text]["answerGroup"] = {};
            questionGroup[question.text]["answerGroup"][answer] = question.answers;
    return render(request, 'take_test.html', { 'exam' : exam, 'questions':questionGroup })
    

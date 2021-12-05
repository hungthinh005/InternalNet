from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Function, Topic, Message
from .forms import MeetingForm
from .decentralize import roles


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
        except:
            user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is not correct')
    context ={'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


@login_required(login_url='login') 
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''
    functions = Function.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )

    topics = Topic.objects.all()
    function_count = functions.count()
    function_messages = Message.objects.all()



    context = {'functions': functions, 'topics': topics, 'function_count': function_count, 'function_messages': function_messages}
    return render(request, 'base/home.html', context)

@roles(allowed_roles=['IT','admin'])
def IT(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''
    functions = Function.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    topics = Topic.objects.all()
    function_count = functions.count()
    function_messages = Message.objects.all()
    

    context = {'functions': functions, 'topics': topics, 'function_count': function_count,  'function_messages': function_messages}
    return render(request, 'base/IT.html', context)

@roles(allowed_roles=['Marketing','admin'])
def Marketing(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''
    functions = Function.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))
    topics = Topic.objects.all()
    function_count = functions.count()

    context = {'functions': functions, 'topics': topics, 'function_count': function_count}
    return render(request, 'base/Marketing.html', context)


def function(request, pk):
    function = Function.objects.get(id=pk)
    function_messages = function.message_set.all()
    participants = function.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            function=function,
            body=request.POST.get('body')
        )
        function.participants.add(request.user)
        return redirect('function', pk=function.id)

    context = {'function': function, 'function_messages':function_messages,'participants': participants}
    return render(request, 'base/function.html', context)

@roles(allowed_roles=['admin'])
def createMeeting(request):
    form = MeetingForm()
    if request.method =='POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/meeting_form.html', context)

@roles(allowed_roles=['admin'])
def updateMeeting(request, pk):
    function = Function.objects.get(id=pk)
    form = MeetingForm(instance=function)

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=function)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/meeting_form.html', context)

@roles(allowed_roles=['admin'])
def deleteMeeting(request, pk): 
    function = Function.objects.get(id=pk)

    if request.method == 'POST':
        function.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':function})


def deleteMessage(request, pk): 
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

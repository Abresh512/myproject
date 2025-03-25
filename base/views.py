from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm

# Create your views here.


def index(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(description__icontains=q)|
                                Q(name__icontains=q))


    topic = Topic.objects.all()
    counted = rooms.count()

    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'room':rooms, 'topic':topic, 'counted':counted, 'room_message':room_message}
    return render(request, "base/Home.html", context)

def login_room(request):
    page ='login'

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            print("Invalid")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            print("Error occured.")

    context = {'page':page}
    return render(request, "base/login.html", context)


def logout_room(request):
    logout(request)
    return redirect('login')


def register_room(request):
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.capitalize()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Operation Failed, please try again")
    context={'form':form}
    return render(request, 'base/login.html', context)


def room(request, pk):
    room = Room.objects.get(id = pk)
    roomMessage = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)


    context = {'room':room, 'roomMessage':roomMessage, 'participants':participants}
    return render(request, "base/room.html", context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('index')
    return render(request, 'base/room_form.html', {'form':form})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    room = user.room_set.all()
    roomMessage = user.message_set.all()
    topic = Topic.objects.all()

    context = {'user':user, 'room':room, 'room_message':roomMessage, 'topic':topic}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def updateroom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("Yourn't allowed here!")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    return render(request, 'base/room_form.html', {'form':form})


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("Yourn't allowed here!")

    if request.method == 'POST':
        room.delete()
        return redirect('index')
    return render(request, 'base/delete.html', {'room':room})



@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("Yourn't allowed here!")

    if request.method == 'POST':
        message.delete()
        return redirect('index')
    return render(request, 'base/delete.html', {'room':message})

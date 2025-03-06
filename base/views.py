from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.


def index(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)


    topic = Topic.objects.all()
    counted = rooms.count()
    context = {'room':rooms, 'topic':topic, 'counted':counted}
    return render(request, "base/Home.html", context)

def room(request, pk):
    room = Room.objects.get(id = pk)
    return render(request, "base/room.html", {'room':room})


def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'base/room_form.html', {'form':form})


def updateroom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    return render(request, 'base/room_form.html', {'form':form})


def deleteroom(request, pk):
    form = Room.objects.get(id=pk)
    if request.method == 'POST':
        form.delete()
        return redirect('index')
    return render(request, 'base/delete.html', {'room':form})
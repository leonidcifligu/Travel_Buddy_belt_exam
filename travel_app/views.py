from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.core.exceptions import PermissionDenied


def index(request):
    if "user_id" in request.session:
        return redirect('/travels')
    return render(request, "index.html")


def login(request):
    if not User.objects.authenticate(request.POST['username'], request.POST['password']):
        messages.error(request, "Invalid username or password")
        return redirect('/')
    user = User.objects.get(username=request.POST['username'])
    request.session['user_id'] = user.id
    return redirect('/travels')


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        user = User.objects.register(request.POST)
        request.session['user_id'] = user.id
        return redirect('/travels')


def logout(request):
    request.session.flush()
    return redirect('/')


def travels(request):
    if "user_id" not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    ids = []
    for i in user.added_travels.all():
        ids.append(i.id)
    travel = Travel.objects.exclude(id__in=ids)
    context = {
        'user': user,
        'travels': travel
    }
    return render(request, "travels.html", context)


def addTravel(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, "travel.html")


def createTravel(request):
    errors = Travel.objects.travel_validator(request.POST)
    if len(errors) > 0:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/travels/add')
    else:
        user = User.objects.get(id=request.session['user_id'])
        travel = Travel.objects.create(
            destination=request.POST['destination'],
            desc=request.POST['desc'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            creator=user,
        )
        user.added_travels.add(travel)
        return redirect('/travels')


def join(request, id):
    user = User.objects.get(id=request.session['user_id'])
    travel = Travel.objects.get(id=id)
    user.added_travels.add(travel)
    return redirect('/travels')


def destination(request, id):
    travel = Travel.objects.get(id=id)
    context = {
        'travel': travel
    }
    return render(request, 'show.html', context)

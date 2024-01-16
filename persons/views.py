from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from persons.models import Person


def index(request):
    message = request.session.pop('message', None)
    context = {
        'message': message,
    }
    return render(request, 'persons/index.html', context)


def login_view(request):
    message = request.session.pop('message', None)
    if request.user.is_authenticated:
        return redirect('person:index')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            message = {
                'type': 'success',
                'text': 'Вы успешно вошли в систему!'
            }
            request.session['message'] = message
            return redirect('persons:index')
        else:
            message = {
                'type': 'danger',
                'text': 'Неверный email или пароль',
            }
            return render(request, 'persons/login.html', {'message': message})
    context = {
        'message': message
    }
    return render(request, 'persons/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('persons:index')

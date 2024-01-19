from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from persons.forms import SignUpForm
from persons.models import Person, Task
from persons.models import TgBot
from persons.smart_tg_bot import SmartTgBot


def index(request):
    person = request.user
    message = request.session.pop('message', None)
    context = {
        'message': message,
        'person': person,
    }
    return render(request, 'persons/index.html', context)


def login_view(request):
    message = request.session.pop('message', None)
    if request.user.is_authenticated:
        return redirect('persons:index')
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


def register_view(request):
    if request.user.is_authenticated:
        return redirect('persons:index')
    message = request.session.pop('message', None)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password_1'])
            person = form.save()
            message = {
                'type': 'success',
                'text': f'Вы успешно зарегистрировались в системе.'
            }
            request.session['message'] = message
            try:
                if 'tg_id' in request.POST:
                    tg_bot = TgBot.objects.get(active_status=True)
                    smart_bot = SmartTgBot(tg_bot)
                    smart_bot.send_msg(f'{person.tg_id}', 'Поздравляю! Вы успешно зарегестрировались!')
                return redirect('persons:login')
            except Exception:
                return redirect('persons:login')
        else:
            message = {
                'type': 'danger',
                'text': f'Ошибка! Пользователь с таким E-mail уже зарегистрирован в системе.'
            }
            request.session['message'] = message
    else:
        form = SignUpForm
    context = {
        'form': form,
        'message': message
    }
    return render(request, 'persons/register.html', context)

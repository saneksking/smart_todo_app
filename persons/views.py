from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from persons.forms import SignUpForm, CreateTaskForm
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


def task_list(request):
    message = request.session.pop('message', None)
    person = request.user
    tasks = Task.objects.filter(person_id=person.id)
    context = {
        'tasks': tasks,
        'message': message,
    }
    return render(request, 'persons/task_list.html', context)


def create_task(request):
    form = CreateTaskForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            person = request.user
            new_task = form.save(commit=False)
            new_task.person_id = person.id
            new_task.save()
            message = {
                'type': 'success',
                'text': f'Задача была успешно добавлена!'
            }
            request.session['message'] = message
            return redirect(reverse('persons:task_list'))
    context = {
        'form': form,
    }
    return render(request, 'persons/create_task.html', context)


def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = CreateTaskForm(request.POST or None, instance=task)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            message = {
                'type': 'success',
                'text': f'Ваша задача успешно изменена!',
            }
            request.session['message'] = message
            return redirect('persons:task_list')
    context = {
        'form': form,
        'task': task,
    }
    return render(request, 'persons/update_task.html', context)


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    message = {
        'type': 'success',
        'text': f'Ваша задача успешно удалена!',
    }
    request.session['message'] = message
    return redirect('persons:task_list')

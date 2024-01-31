from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from persons.forms import SignUpForm, CreateTaskForm, SettingsForm
from persons.models import Person, Task
from persons.models import TgBot
from persons.smart_tg_bot import SmartTgBot
from persons.decorators import is_superuser
from persons.tasks import send_tasks_in_time


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
    paginator = Paginator(tasks, 10)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    context = {
        'objects': objects,
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
                'text': f'Задача была успешно изменена!',
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


def settings(request):
    person = get_object_or_404(Person, id=request.user.id)
    form = SettingsForm(request.POST or None, instance=person)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            message = {
                'type': 'success',
                'text': f'Ваш профиль успешно изменён!',
            }
            request.session['message'] = message
            return redirect('persons:index')
    context = {
        'form': form,
    }
    return render(request, 'persons/settings.html', context)


def end_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = True
    task.save()
    message = {
        'type': 'success',
        'text': f'Статус задачи был успешно изменён!',
    }
    request.session['message'] = message
    return redirect('persons:task_list')


@user_passes_test(is_superuser)
def admin_panel(request):
    message = request.session.pop('message', None)
    person_list = Person.objects.all()
    paginator = Paginator(person_list, 5)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    context = {
        'objects': objects,
        'message': message,
    }
    return render(request, 'persons/admin_panel/admin_panel.html', context)


@user_passes_test(is_superuser)
def admin_panel_delete_person(request, person_id):
    person = Person.objects.get(id=person_id)
    person.delete()
    message = {
        'type': 'success',
        'text': f'Пользователь был успешно удалён!',
    }
    request.session['message'] = message
    return redirect('persons:admin_panel')


@user_passes_test(is_superuser)
def person_profile(request, person_id):
    person = Person.objects.get(id=person_id)
    context = {
        'person': person,
    }
    return render(request, 'persons/admin_panel/person_profile.html', context)


def return_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = None
    task.save()
    message = {
        'type': 'success',
        'text': f'Статус задачи был успешно изменён!',
    }
    request.session['message'] = message
    return redirect('persons:task_list')


def send_tasks(request):
    print('Success')
    response = {
        'type': 'danger',
        'text': 'Внимание! При отправке задач произошла ошибка!'
    }
    request.session['message'] = response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        print('Success 2')
        response = {
            'type': 'success',
            'text': 'Уведомление в Телеграм успешно отправлено!',
        }
        request.session['message'] = response
        send_tasks_in_time.delay()
    return JsonResponse(response)

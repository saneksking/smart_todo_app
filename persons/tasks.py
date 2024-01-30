from persons.models import Person, TgBot
from persons.smart_tg_bot import SmartTgBot
from smart_todo_app.celery import app
import datetime


@app.task
def task_test():
    print(f'*** Запускаю тестовую задачу Celery ***')
    print(f'Тестовая задача выполнена.')
    print(f'=== FINISH ===')


@app.task
def send_tasks_in_time():
    try:
        tg_bot = TgBot.objects.filter(active_status=True).first()
        # print(tg_bot)
        smart_bot = SmartTgBot(tg_bot)
        date = datetime.date.today()
        # print(date)
        person_list = Person.objects.exclude(tg_id='').filter(task__time_end=date).distinct()
        # print(person_list)
        for person in person_list:
            task_list = person.task.filter(time_end=date)
            # print(task_list)
            count = task_list.count()
            # print(count)
            msg = f'Приветствую, {person.full_name()}. На сегодня у вас задач {task_list.count()}:\n\n'
            # print(msg)
            for n, task in enumerate(task_list, 1):
                # print(f'{task.time_end}')
                msg += f'Задача №{n}: {task.title}\n'
            # print(msg)
            smart_bot.send_msg(person.tg_id, msg)
    except Exception as e:
        print(e)

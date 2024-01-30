from smart_todo_app.celery import app


@app.task
def task_test():
    print(f'*** Запускаю тестовую задачу Celery ***')
    print(f'Тестовая задача выполнена.')
    print(f'=== FINISH ===')

Smart To Do App

---

- Установить Celery
- Установить Redis: ```sudo pacman -S redis```
- Команда для запуска Redis в Linux: ```sudo systemctl restart redis.service```

Команда для запуска Celery: ```celery -A smart_todo_app worker -l info -B```

Команда для запуска MariaDB в Linux: ```sudo systemctl start mariadb```


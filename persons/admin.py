from django.contrib import admin
from persons.models import Person, Task, TgBot


admin.site.register(Person)
admin.site.register(Task)
admin.site.register(TgBot)

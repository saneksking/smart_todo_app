from django.contrib.auth.decorators import login_required
from django.urls import path
from persons import views


app_name = 'persons'

urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('tasks/', login_required(views.task_list), name='task_list'),
    path('tasks/create/', login_required(views.create_task), name='create_task'),
    path('tasks/update/<int:task_id>/', login_required(views.update_task), name='update_task'),
    path('tasks/delete/<int:task_id>/', login_required(views.delete_task), name='delete_task'),
    path('settings/', login_required(views.settings), name='settings'),
]
